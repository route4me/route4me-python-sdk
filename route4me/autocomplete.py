"""The :class:`Autocomplete` resource: complete a partly typed address (API V4)."""

from .api_endpoints import AUTOCOMPLETE
from .base import Base


class Autocomplete(Base):
    """Address autocomplete: suggestions for a partly typed address (API V4).

    Use it as ``route4me.autocomplete``. Requests go to ``/autocomplete.php``.

    The endpoint is in no OpenAPI spec and no other SDK, so its parameter
    names are not documented: the keywords are sent as the query, as given.

    Every method returns the decoded JSON reply, the raw body (``bytes``) when
    it is not JSON, or on an API error the ``{"errors": ...}`` dict from
    :meth:`APIException.to_dict <route4me.exceptions.APIException.to_dict>`
    instead of raising.

    .. versionadded:: 1.0.0
    """

    def autocomplete_address(self, **kwargs):
        """Get address suggestions for a partly typed address.

        Sends ``GET /autocomplete.php`` with the keywords as the query.

        Without the address the API answers ``No address specified``.

        :param kwargs: query parameters, sent as is. ``address``, the partial
            address, is the one that matters (checked against the live API).
        :return: the decoded JSON reply, the raw body (``bytes``) when it is
            not JSON, or the ``{"errors": ...}`` dict on an API error.

        .. versionadded:: 1.0.0
        """
        return self._request_decoded(AUTOCOMPLETE, dict(kwargs), "get")
