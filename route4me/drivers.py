"""The :class:`Drivers` resource: the drivers of the account (API V4)."""

from .api_endpoints import VIEW_DRIVERS
from .base import Base


class Drivers(Base):
    """Drivers: the members of the account who drive routes (API V4).

    Use it as ``route4me.drivers``. Requests go to
    ``/api/drivers/view_drivers.php``. For the full team, with filters, see
    :meth:`TeamV5.get_team_members <route4me.team_v5.TeamV5.get_team_members>`.

    Every method returns the decoded JSON reply, the raw body (``bytes``) when
    it is not JSON, or on an API error the ``{"errors": ...}`` dict from
    :meth:`APIException.to_dict <route4me.exceptions.APIException.to_dict>`
    instead of raising.

    .. versionadded:: 1.0.0
    """

    def get_drivers(self, **kwargs):
        """List the drivers of the account.

        Sends ``GET /api/drivers/view_drivers.php``.

        :param kwargs: query parameters, sent as is.
        :return: the decoded JSON reply: a list of drivers, the raw body
            (``bytes``) when it is not JSON, or the ``{"errors": ...}`` dict on
            an API error.

        .. versionadded:: 1.0.0
        """
        return self._request_decoded(VIEW_DRIVERS, dict(kwargs), "get")
