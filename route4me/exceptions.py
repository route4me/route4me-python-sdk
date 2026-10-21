"""Exceptions raised by the SDK.

:class:`APIException` is raised when the API answers with an HTTP error;
:class:`ParamValueException` when a parameter is missing or invalid.
"""

import json

from ._redact import redact_url
from .config import Route4MeConfig
from .version import VERSION_STRING

DRIVER_VERSION = f"route4me-python-sdk-{VERSION_STRING}"


def _message_list(value):
    """Flatten an error value from a reply into a list of strings.

    :param value: a string, a list of strings, a dict of field name to
        messages (the V5 ``messages`` shape), or ``None``.
    :return: the messages, each one a string; empty for ``None`` or an empty
        value.
    """
    if value is None or value == "":
        return []
    if isinstance(value, dict):
        value = list(value.values())
    if not isinstance(value, (list, tuple)):
        return [str(value)]
    flattened = []
    for item in value:
        flattened.extend(_message_list(item))
    return flattened


class APIException(Exception):
    """The API answered with an HTTP status outside the 200-399 range.

    Most resource methods catch it and return :meth:`to_dict` instead of
    raising it.

    :param status_code: the HTTP status code.
    :param response: the response body text. The client removes the API key
        from it before raising.
    :param url: the request URL.
    :param redact: whether to strip credentials from ``url``. ``None`` (the
        default) follows ``Route4MeConfig.redact_urls``.

    .. versionchanged:: 0.2.0
       ``url`` is now redacted. ``requests`` resolves ``Response.url`` to the
       fully expanded request URL, which for the V4 API carries
       ``?api_key=<plaintext>``; that string used to appear in ``str(exc)``,
       ``repr(exc)`` and every traceback frame, and was forwarded verbatim to
       any error-reporting service that serialises exception attributes.

       The raw URL is deliberately **not** kept anywhere on the instance. A
       private attribute would still escape through ``vars(exc)``,
       ``exc.__dict__``, ``copy``, ``pickle`` and Sentry/Datadog -- the
       security posture of a public attribute with the discoverability of a
       private one. Set ``Route4MeConfig.redact_urls = False`` to opt out
       globally.
    """

    def __init__(self, status_code, response, url, redact=None):
        self.status_code = status_code
        self.response = response
        if redact is None:
            redact = Route4MeConfig.redact_urls
        #: Request URL with credentials stripped. Safe to log.
        self.url = redact_url(url) if redact else url
        exception = {
            "http_status_code": status_code,
            "response": response,
            "url": self.url,
            "driver_version": DRIVER_VERSION,
        }
        Exception.__init__(self, exception)

    def get_status_code(self):
        """Return the HTTP status code.

        :return: the status code, e.g. ``404``.
        """
        return self.status_code

    def get_response(self):
        """Return the response body.

        :return: the response body text.
        """
        return self.response

    def get_url(self):
        """Return the request URL.

        :return: the URL, with credentials stripped unless redaction was
            turned off.
        """
        return self.url

    def to_dict(self):
        """Return the error as a dict.

        Always shaped ``{"errors": [message, ...]}``: this is what almost every
        resource method returns on an API error, so the shape is load-bearing.
        ``". ".join(result["errors"])`` always works.

        Defensive on three inputs that used to raise *out of the error path*,
        turning a plain HTTP failure into a confusing traceback:

        * a ``None`` or ``bytes`` body -- ``json.JSONDecodeError`` does not
          cover the resulting ``TypeError``
        * a body that is valid JSON but not an object, e.g. ``[1, 2]`` --
          ``json.loads`` returns a list, whose ``.get`` raises ``AttributeError``
        * a V5 error envelope, which has no ``errors`` key at all

        :return: ``{"errors": messages}``, a non-empty list of strings: the V4
            ``errors``, the V5 ``messages`` flattened, or the ``message``
            value; ``["Unexpected server response"]`` when none of them is
            present or the body is not a JSON object.

        .. versionchanged:: 1.0.0
           ``errors`` is always a list of strings. It used to be a string for a
           non-JSON body, and ``None`` when the reply had no ``errors`` key.
        """
        try:
            payload = json.loads(self.response)
        except (TypeError, ValueError):
            # ValueError covers json.JSONDecodeError, which subclasses it.
            payload = None

        messages = []
        if isinstance(payload, dict):
            # V4 replies carry {"errors": [...]}. V5 replies have no "errors"
            # key (DataTypes/V5/ResultResponse.cs):
            #   {"status": false, "code": 422, "messages": {"field": ["..."]}}
            # Without the fallbacks every V5 failure lost its message.
            for key in ("errors", "messages", "message"):
                messages = _message_list(payload.get(key))
                if messages:
                    break
        return {"errors": messages or ["Unexpected server response"]}


class ParamValueException(Exception):
    """A parameter is missing or has an invalid value.

    Raised before any request is sent.

    :param param: name of the offending parameter, or a group name such as
        ``"params"`` when required parameters are missing.
    :param msg: what is wrong with it.
    """

    def __init__(self, param, msg):
        self.param = param
        self.msg = msg
        exception = {
            "param": param,
            "msg": msg,
        }
        Exception.__init__(self, exception)

    def get_msg(self):
        """Return the error message.

        :return: the message passed as ``msg``.
        """
        return self.msg
