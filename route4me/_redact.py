"""Redaction helpers for URLs, headers and response bodies.

Every function here is **total**: on any internal failure it degrades to a
coarser redaction rather than raising. These run on the error path, and a
redactor that throws would turn a plain 401 into an unhelpful traceback
originating inside the SDK.

Why this exists: ``requests`` resolves ``Response.url`` to the fully expanded
request URL. The V4 API authenticates by query string, so that URL carries
``?api_key=<plaintext>``. Anything that stringifies an exception -- a log line,
a traceback, Sentry, Datadog -- would otherwise publish a live credential.
"""

import re
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

#: Replacement text. Conspicuous enough that a log reader can tell redaction
#: happened rather than seeing an empty or missing value, and deliberately
#: URL-safe: any character needing percent-encoding would come back out of
#: ``urlencode`` as ``%2A%2A%2AREDACTED%2A%2A%2A``, which is unreadable in
#: exactly the place this matters most.
REDACTED = "REDACTED"

#: Query-string parameters whose values must never reach a log or a traceback.
#: Matched case-insensitively.
SENSITIVE_PARAMS = frozenset(
    {
        "api_key",
        "apikey",
        "api-key",
        "key",
        "token",
        "access_token",
        "auth_token",
        "refresh_token",
        "session_guid",
        "member_session_id",
        "session_id",
        "password",
        "passwd",
        "strpassword",
        "strpassword_1",
        "strpassword_2",
        "secret",
        "client_secret",
        "signature",
    }
)

#: Request/response headers whose values must never be logged.
SENSITIVE_HEADERS = frozenset(
    {
        "authorization",
        "proxy-authorization",
        "cookie",
        "set-cookie",
        "x-api-key",
        "x-auth-token",
    }
)


def _drop_query(url):
    """Coarse fallback: discard everything after the first ``?``.

    Used when a URL cannot be parsed. Throwing the whole query string away is
    the safe choice -- we would rather lose debugging detail than emit a
    credential we failed to recognise.
    """
    try:
        return url.split("?", 1)[0] + "?" + REDACTED
    except Exception:
        return REDACTED


def redact_url(url):
    """Return ``url`` with the values of sensitive query parameters replaced.

    The host, path and non-sensitive parameters are preserved, so the result is
    still useful for debugging -- you can see *which* endpoint failed.

    >>> redact_url("https://api.route4me.com/x.php?api_key=abc123&limit=1")
    'https://api.route4me.com/x.php?api_key=REDACTED&limit=1'

    Falls back to :func:`_drop_query` if the URL cannot be parsed. Never raises.
    """
    if not url or not isinstance(url, str):
        return url
    try:
        parts = urlsplit(url)
        if not parts.query:
            return url
        pairs = parse_qsl(parts.query, keep_blank_values=True)
        cleaned = [(k, REDACTED if k.lower() in SENSITIVE_PARAMS else v) for k, v in pairs]
        return urlunsplit(parts._replace(query=urlencode(cleaned)))
    except Exception:
        return _drop_query(url)


def redact_text(text, *secrets):
    """Return ``text`` with every non-empty value in ``secrets`` replaced.

    Used on response bodies: several Route4Me V4 endpoints echo the request
    parameters back inside error payloads, which means the API key can appear
    in the body as well as the URL.

    Short secrets are ignored -- replacing a 1- or 2-character string would
    corrupt the body without protecting anything meaningful.
    """
    if not text or not isinstance(text, str):
        return text
    try:
        for secret in secrets:
            if isinstance(secret, str) and len(secret) >= 8:
                text = text.replace(secret, REDACTED)
                # Also catch a percent- or URL-encoded appearance.
                text = re.sub(re.escape(secret), REDACTED, text, flags=re.IGNORECASE)
        return text
    except Exception:
        return REDACTED


def redact_headers(headers):
    """Return a copy of ``headers`` with sensitive values replaced.

    Accepts anything dict-like (including ``requests``' case-insensitive
    ``CaseInsensitiveDict``). Returns a plain ``dict``.
    """
    if not headers:
        return {}
    try:
        return {k: (REDACTED if str(k).lower() in SENSITIVE_HEADERS else v) for k, v in dict(headers).items()}
    except Exception:
        return {REDACTED: REDACTED}


def redact_params(params):
    """Return a copy of a query-parameter mapping with sensitive values replaced."""
    if not params:
        return {}
    try:
        return {k: (REDACTED if str(k).lower() in SENSITIVE_PARAMS else v) for k, v in dict(params).items()}
    except Exception:
        return {REDACTED: REDACTED}
