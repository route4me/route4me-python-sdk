"""The :class:`AssetTracking` resource: find an asset by its tracking number (API V4)."""

from .api_endpoints import ASSET_TRACKING
from .base import Base


class AssetTracking(Base):
    """Asset tracking: where a tracked asset or order is (API V4).

    Use it as ``route4me.asset_tracking``. Requests go to
    ``/api.v4/status.php``.

    Every method returns the decoded JSON reply, or on an API error the
    ``{"errors": ...}`` dict from :meth:`APIException.to_dict
    <route4me.exceptions.APIException.to_dict>` instead of raising.

    .. versionadded:: 1.0.0
    """

    def find_asset(self, tracking):
        """Get the location and status of an asset from its tracking number.

        Sends ``GET /api.v4/status.php`` with ``tracking`` in the query.

        :param tracking: the tracking number of the asset.
        :return: the decoded JSON reply, or the ``{"errors": ...}`` dict on an
            API error, e.g. for an unknown tracking number.

        .. versionadded:: 1.0.0
        """
        return self._call_api(ASSET_TRACKING, "get", {"tracking": tracking})
