import json

from ._redact import redact_url
from .config import Route4MeConfig
from .version import VERSION_STRING

DRIVER_VERSION = f"route4me-python-sdk-{VERSION_STRING}"


class APIException(Exception):
    """
    Handle API Exceptions

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
        """
        Status code
        :return:
        """
        return self.status_code

    def get_response(self):
        """
        Return response
        :return:
        """
        return self.response

    def get_url(self):
        """
        Redacted request URL
        :return:
        """
        return self.url

    def to_dict(self):  # pylint: disable=too-many-return-statements  # one return per documented error shape
        """
        Return a dictionary representation of the exception

        Always shaped ``{"errors": ...}`` -- this is what almost every resource
        method returns on an API error, so the shape is load-bearing.

        Defensive on three inputs that used to raise *out of the error path*,
        turning a plain HTTP failure into a confusing traceback:

        * a ``None`` or ``bytes`` body -- ``json.JSONDecodeError`` does not
          cover the resulting ``TypeError``
        * a body that is valid JSON but not an object, e.g. ``[1, 2]`` --
          ``json.loads`` returns a list, whose ``.get`` raises ``AttributeError``
        * a V5 error envelope, which has no ``errors`` key at all
        """
        try:
            payload = json.loads(self.response)
        except (TypeError, ValueError):
            # ValueError covers json.JSONDecodeError, which subclasses it.
            return {"errors": "Unexpected server response"}

        if not isinstance(payload, dict):
            return {"errors": "Unexpected server response"}

        if payload.get("errors") is not None:
            # V4 shape: {"errors": [...]}
            return {"errors": payload["errors"]}

        # V5 shape (DataTypes/V5/ResultResponse.cs):
        #   {"status": false, "code": 422, "messages": {"field": ["..."]}}
        # There is no "errors" key, so without this branch every V5 failure
        # returned {"errors": None} and threw the actual message away.
        messages = payload.get("messages")
        if isinstance(messages, dict):
            flattened = []
            for value in messages.values():
                if isinstance(value, (list, tuple)):
                    flattened.extend(value)
                else:
                    flattened.append(value)
            return {"errors": flattened}
        if messages:
            return {"errors": messages}

        if "errors" in payload:
            # Present but explicitly null -- preserve the historical shape.
            return {"errors": payload["errors"]}

        return {"errors": payload.get("message") or "Unexpected server response"}


class ParamValueException(Exception):
    """
    Handle Params exceptions
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
        """
        Message from exception
        :return:
        """
        return self.msg
