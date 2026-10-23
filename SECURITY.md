# Security policy

## Reporting a vulnerability

Please do not open a public GitHub issue for a security problem.

Email **support@route4me.com** with "Security: route4me-python-sdk" in the subject. Include the affected version and the steps to reproduce. We will acknowledge your report and keep you informed until a fix is released.

If you have committed a Route4Me API key anywhere public, rotate it in your Route4Me account at once. Removing it from git history does not invalidate it.

## Supported versions

| Version | Supported |
|---|---|
| 1.x | Yes |
| 0.x | No. Upgrade to 1.x |

The SDK supports every Python release from 3.9 up.

## How the SDK protects your API key

- Every request goes over HTTPS to a Route4Me host. The test suite fails if any request leaves `api.route4me.com`, `wh.route4me.com`, `rapid.route4me.com` or `validator.route4me.com`, or goes over plain HTTP.
- API V5 requests send the key as an `Authorization: Bearer` header, so it never appears in a URL or a server log. The V4 API requires it as the `api_key` query parameter. It is never put in a request body.
- `APIException` messages, URLs and logged errors are redacted (`route4me/_redact.py`), so the key does not end up in logs.
- Values placed in a URL path are percent-encoded, so a crafted ID cannot redirect a request to another endpoint.
- No request state is kept between calls: one call's parameters never travel with the next.

## Dependencies on Python 3.9

On Python 3.10 and later the SDK requires `requests>=2.33.0` and `urllib3>=2.8.0`, which have no known advisories.

Those releases do not support Python 3.9. There the SDK installs the newest available versions (`requests` 2.32.5, `urllib3` 2.6.3), which still carry these advisories:
- `requests`: CVE-2026-25645;
- `urllib3`: CVE-2026-44431, CVE-2026-44432, CVE-2026-97687, CVE-2026-97688 and CVE-2026-97689.

Their impact on SDK traffic is limited:
- requests follows redirects itself rather than through urllib3's redirect API, so CVE-2026-44431 does not apply to it;
- the decompression advisories need a malicious server.

Still, upgrade to Python 3.10 or later where you can. Support for 3.9 will be dropped in a future minor release.
