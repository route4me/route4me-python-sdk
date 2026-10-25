"""The :class:`TrackingHistory` resource (API V5): export the GPS tracking history."""

from .api_endpoints import TRACKING_HISTORY_EXPORT_V5
from .base import Base


class TrackingHistory(Base):
    """Tracking history: the recorded GPS positions of members and devices (API V5).

    Use it as ``route4me.tracking_history``. The method sends a request to
    ``/modules/api/v5.0/tracking-history`` on ``wh.route4me.com``.

    .. versionadded:: 1.0.0
    """

    def export_tracking_history(self, **kwargs):
        """Export the tracking history as a file.

        Sends ``POST /modules/api/v5.0/tracking-history/export`` with the
        keywords as the JSON body.

        :param kwargs: the export fields, all optional: ``member_id``,
            ``device_id`` or ``route_id``, whose history to export;
            ``format``, ``"csv"``, ``"json"`` or ``"xml"``; ``time_period``,
            e.g. ``"today"``, ``"yesterday"`` or ``"7days"``, or ``start_date``
            and ``end_date`` as Unix timestamps; ``last_position``;
            ``show_cd``, to include custom data; ``show_mmd``; ``download``;
            ``tz``, the time zone; and ``columns``, the CSV columns.
        :return: the decoded JSON reply for the JSON format, the file as
            ``bytes`` for the CSV and XML formats, or the ``{"errors": ...}``
            dict on an API error.

        .. versionadded:: 1.0.0
        """
        return self._request_decoded(TRACKING_HISTORY_EXPORT_V5, {}, "post", json=kwargs)
