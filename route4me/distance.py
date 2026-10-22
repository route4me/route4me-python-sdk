"""The :class:`Distance` resource: the distance between two addresses (API V4)."""

from .api_endpoints import DISTANCE
from .base import Base


class Distance(Base):
    """Distance: the driving distance between two addresses (API V4).

    Use it as ``route4me.distance``. Requests go to ``/api/distance.php``.

    The endpoint is in no OpenAPI spec and no other SDK, so its parameter
    names are not documented: the keywords are sent as the query, as given.

    Every method returns the decoded JSON reply, the raw body (``bytes``) when
    it is not JSON, or on an API error the ``{"errors": ...}`` dict from
    :meth:`APIException.to_dict <route4me.exceptions.APIException.to_dict>`
    instead of raising.

    .. versionadded:: 1.0.0
    """

    def calculate_distance(self, **kwargs):
        """Calculate the distance between a start and an end address.

        Sends ``GET /api/distance.php`` with the keywords as the query.

        Without a valid start and end address the API answers with the plain
        text ``Missing or invalid start and end address.``, which comes back
        as ``bytes``.

        :param kwargs: query parameters, sent as is: the start and end
            addresses.
        :return: the decoded JSON reply, the raw body (``bytes``) when it is
            not JSON, or the ``{"errors": ...}`` dict on an API error.

        .. versionadded:: 1.0.0
        """
        return self._request_decoded(DISTANCE, dict(kwargs), "get")
