"""The :class:`RecurringRoutes` resource (API V5): schedules, route schedules, master routes and their copies."""

from ._url import path_segment
from .api_endpoints import (
    RECURRING_MASTER_ROUTES_V5,
    RECURRING_ROUTE_SCHEDULES_REPLACE_V5,
    RECURRING_ROUTE_SCHEDULES_V5,
    RECURRING_SCHEDULED_ROUTES_GET_COPIES_V5,
    RECURRING_SCHEDULED_ROUTES_IS_COPY_V5,
    RECURRING_SCHEDULES_V5,
    SCHEDULE_CALENDAR,
)
from .base import Base
from .exceptions import ParamValueException


class RecurringRoutes(Base):
    """Recurring routes: schedules, the routes they repeat, and the copies made from them.

    Use it as ``route4me.recurring_routes``. It mirrors the C#
    ``SchedulesManagerV5``. A *schedule* says when something repeats; a
    *route schedule* attaches a schedule to a route; a *master route* is a
    route created together with its schedule. Requests go to
    ``/modules/api/v5.0/recurring-routes/...`` on ``wh.route4me.com``, except
    :meth:`get_schedule_calendar`, which is API V4.

    Unless stated otherwise, a method returns the decoded JSON reply, or on an
    API error the ``{"errors": ...}`` dict from :meth:`APIException.to_dict
    <route4me.exceptions.APIException.to_dict>` instead of raising.

    .. versionadded:: 1.0.0
    """

    #: Body fields the spec requires to create a schedule.
    SCHEDULE_CREATE_FIELDS = ("name", "schedule", "advance_interval", "advance_schedule_interval_days", "timezone")
    #: Body fields the spec requires to create a route schedule.
    ROUTE_SCHEDULE_CREATE_FIELDS = ("route_id", "schedule_uid")
    #: Body fields the spec requires to update a route schedule.
    ROUTE_SCHEDULE_UPDATE_FIELDS = ("route_uid", "schedule_uid", "root_member_id")
    #: Body fields the spec requires to replace a route schedule.
    ROUTE_SCHEDULE_REPLACE_FIELDS = ("schedule",)
    #: Body fields the spec requires to create a master route.
    MASTER_ROUTE_CREATE_FIELDS = ("route_id", "schedule")
    #: Query parameters the spec requires for a route schedule preview.
    ROUTE_SCHEDULE_PREVIEW_PARAMS = ("start", "end")
    #: Body fields the spec requires to list the copies of a scheduled route.
    ROUTE_SCHEDULE_COPIES_FIELDS = ("route_id",)

    def __init__(self, api):
        """Create the resource.

        :param api: the :class:`~route4me.api.Route4Me` client.
        """
        Base.__init__(self, api)

    def _require(self, values, names):
        """Raise when a required field is missing.

        :param values: the fields given.
        :param names: the names that must be present.
        :raise ParamValueException: naming every missing field.
        """
        missing = self._missing(values, names)
        if missing:
            raise ParamValueException(", ".join(missing), "Missing required params")

    @staticmethod
    def _url(base, value, name, suffix=""):
        """Build a URL with one ID encoded as a path segment.

        :param base: the URL before the ID.
        :param value: the ID.
        :param name: the parameter name, reported when the ID is empty.
        :param suffix: path after the ID, e.g. ``"/items"``.
        :return: the absolute URL.
        :raise ParamValueException: when the ID is empty.
        """
        return f"{base}/{path_segment(value, name)}{suffix}"

    # ------------------------------------------------------------ schedules

    def get_schedules_list(self):
        """List the schedules of the account.

        Sends ``GET /modules/api/v5.0/recurring-routes/schedules``.

        :return: the decoded JSON reply, with the schedules under ``data``, or
            the ``{"errors": ...}`` dict on an API error.

        .. versionadded:: 1.0.0
        """
        return self._call_api(RECURRING_SCHEDULES_V5, "get", {})

    def create_schedule(self, **kwargs):
        """Create a schedule.

        Sends ``POST /modules/api/v5.0/recurring-routes/schedules`` with the
        keywords as the JSON body.

        :param kwargs: the schedule. Required: ``name``; ``schedule``, a list
            of recurrence rules; ``advance_interval``;
            ``advance_schedule_interval_days``; and ``timezone``, e.g.
            ``"UTC"``. Optional: ``schedule_blacklist``, a list of
            ``YYYY-MM-DD`` dates to skip.
        :return: the decoded JSON reply, with the new schedule under ``data``,
            or the ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when a required field is missing.

        .. versionadded:: 1.0.0
        """
        self._require(kwargs, self.SCHEDULE_CREATE_FIELDS)
        return self._call_api(RECURRING_SCHEDULES_V5, "post", {}, body=dict(kwargs))

    def get_schedule(self, schedule_uid):
        """Get a schedule.

        Sends ``GET /modules/api/v5.0/recurring-routes/schedules/{schedule_uid}``.

        :param schedule_uid: ID of the schedule.
        :return: the decoded JSON reply, with the schedule under ``data``, or
            the ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when ``schedule_uid`` is empty.

        .. versionadded:: 1.0.0
        """
        return self._call_api(self._url(RECURRING_SCHEDULES_V5, schedule_uid, "schedule_uid"), "get", {})

    def update_schedule(self, schedule_uid, **kwargs):
        """Update a schedule.

        Sends ``PUT /modules/api/v5.0/recurring-routes/schedules/{schedule_uid}``
        with the keywords as the JSON body.

        :param schedule_uid: ID of the schedule.
        :param kwargs: the values to change: ``name``, ``schedule``,
            ``schedule_blacklist``, ``advance_interval``,
            ``advance_schedule_interval_days`` or ``timezone``.
        :return: the decoded JSON reply, with the schedule under ``data``, or
            the ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when ``schedule_uid`` is empty.

        .. versionadded:: 1.0.0
        """
        url = self._url(RECURRING_SCHEDULES_V5, schedule_uid, "schedule_uid")
        return self._call_api(url, "put", {}, body=dict(kwargs))

    def delete_schedule(self, schedule_uid, with_routes=False):
        """Delete a schedule, and optionally the routes made from it.

        Sends ``DELETE /modules/api/v5.0/recurring-routes/schedules/{schedule_uid}``
        with ``with-routes`` in the query, as ``1`` or ``0``.

        :param schedule_uid: ID of the schedule.
        :param with_routes: ``True`` to also delete the routes associated with
            the schedule.
        :return: the decoded JSON reply, or the ``{"errors": ...}`` dict on an
            API error.
        :raise ParamValueException: when ``schedule_uid`` is empty.

        .. versionadded:: 1.0.0
        """
        url = self._url(RECURRING_SCHEDULES_V5, schedule_uid, "schedule_uid")
        return self._call_api(url, "delete", {"with-routes": int(bool(with_routes))})

    # ------------------------------------------------------ route schedules

    def get_route_schedules_list(self):
        """List the route schedules of the account.

        Sends ``GET /modules/api/v5.0/recurring-routes/route-schedules``.

        :return: the decoded JSON reply, with the route schedules under
            ``data``, or the ``{"errors": ...}`` dict on an API error.

        .. versionadded:: 1.0.0
        """
        return self._call_api(RECURRING_ROUTE_SCHEDULES_V5, "get", {})

    def create_route_schedule(self, **kwargs):
        """Attach a schedule to a route.

        Sends ``POST /modules/api/v5.0/recurring-routes/route-schedules`` with
        the keywords as the JSON body.

        :param kwargs: the route schedule. Required: ``route_id`` and
            ``schedule_uid``. Optional: ``member_id`` and ``vehicle_id``.
        :return: the decoded JSON reply, with the route schedule under
            ``data``, or the ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when a required field is missing.

        .. versionadded:: 1.0.0
        """
        self._require(kwargs, self.ROUTE_SCHEDULE_CREATE_FIELDS)
        return self._call_api(RECURRING_ROUTE_SCHEDULES_V5, "post", {}, body=dict(kwargs))

    def get_route_schedule(self, route_id):
        """Get the schedule of a route.

        Sends ``GET /modules/api/v5.0/recurring-routes/route-schedules/{route_id}``.

        :param route_id: ID of the route.
        :return: the decoded JSON reply, with the route schedule under
            ``data``, or the ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when ``route_id`` is empty.

        .. versionadded:: 1.0.0
        """
        return self._call_api(self._url(RECURRING_ROUTE_SCHEDULES_V5, route_id, "route_id"), "get", {})

    def update_route_schedule(self, route_id, **kwargs):
        """Update the schedule of a route.

        Sends ``PUT /modules/api/v5.0/recurring-routes/route-schedules/{route_id}``
        with the keywords as the JSON body.

        :param route_id: ID of the route.
        :param kwargs: the route schedule. Required: ``route_uid``,
            ``schedule_uid`` and ``root_member_id``. Optional: ``member_id``
            and ``vehicle_id``.
        :return: the decoded JSON reply, with the route schedule under
            ``data``, or the ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when ``route_id`` is empty or a required
            field is missing.

        .. versionadded:: 1.0.0
        """
        url = self._url(RECURRING_ROUTE_SCHEDULES_V5, route_id, "route_id")
        self._require(kwargs, self.ROUTE_SCHEDULE_UPDATE_FIELDS)
        return self._call_api(url, "put", {}, body=dict(kwargs))

    def delete_route_schedule(self, route_id):
        """Delete every schedule of a route.

        Sends ``DELETE /modules/api/v5.0/recurring-routes/route-schedules/{route_id}``.

        :param route_id: ID of the route.
        :return: the decoded JSON reply, e.g. ``{"status": true}``, or the
            ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when ``route_id`` is empty.

        .. versionadded:: 1.0.0
        """
        return self._call_api(self._url(RECURRING_ROUTE_SCHEDULES_V5, route_id, "route_id"), "delete", {})

    def delete_route_schedule_items(self, route_id):
        """Delete the schedule items of a route.

        Sends ``DELETE /modules/api/v5.0/recurring-routes/route-schedules/{route_id}/items``.

        :param route_id: ID of the route.
        :return: the decoded JSON reply, or the ``{"errors": ...}`` dict on an
            API error.
        :raise ParamValueException: when ``route_id`` is empty.

        .. versionadded:: 1.0.0
        """
        url = self._url(RECURRING_ROUTE_SCHEDULES_V5, route_id, "route_id", "/items")
        return self._call_api(url, "delete", {})

    def get_route_schedule_preview(self, route_id, **kwargs):
        """Preview the dates on which the schedule of a route repeats.

        Sends ``GET /modules/api/v5.0/recurring-routes/route-schedules/{route_id}/preview``
        with the keywords as the query.

        :param route_id: ID of the route.
        :param kwargs: query parameters. Required: ``start`` and ``end``, the
            date range as ``YYYY-MM-DD``.
        :return: the decoded JSON reply, with the dates under ``dates``, or
            the ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when ``route_id`` is empty, or ``start``
            or ``end`` is missing.

        .. versionadded:: 1.0.0
        """
        url = self._url(RECURRING_ROUTE_SCHEDULES_V5, route_id, "route_id", "/preview")
        self._require(kwargs, self.ROUTE_SCHEDULE_PREVIEW_PARAMS)
        return self._call_api(url, "get", dict(kwargs))

    def replace_route_schedule(self, route_id, **kwargs):
        """Replace the schedule of a route with a new one.

        Sends ``PUT /modules/api/v5.0/recurring-routes/route-schedules/replace/{route_id}``
        with the keywords as the JSON body.

        :param route_id: ID of the route.
        :param kwargs: the new schedule. Required: ``schedule``, a list of
            recurrence rules. Optional: ``route_uid``, ``member_id``,
            ``vehicle_id``, ``schedule_uid``, ``schedule_blacklist``,
            ``advance_interval``, ``advance_schedule_interval_days``,
            ``timezone`` and ``sync``.
        :return: the decoded JSON reply, with the route schedule under
            ``data``, or the ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when ``route_id`` is empty or ``schedule``
            is missing.

        .. versionadded:: 1.0.0
        """
        url = self._url(RECURRING_ROUTE_SCHEDULES_REPLACE_V5, route_id, "route_id")
        self._require(kwargs, self.ROUTE_SCHEDULE_REPLACE_FIELDS)
        return self._call_api(url, "put", {}, body=dict(kwargs))

    # -------------------------------------------------------- master routes

    def create_master_route(self, **kwargs):
        """Create a master route: a route schedule built from an existing route.

        Sends ``POST /modules/api/v5.0/recurring-routes/master-routes`` with
        the keywords as the JSON body.

        :param kwargs: the master route. Required: ``route_id`` and
            ``schedule``, a list of recurrence rules. Optional:
            ``route_name``, ``member_id``, ``vehicle_id``, ``name``,
            ``schedule_blacklist``, ``advance_interval``,
            ``advance_schedule_interval_days``, ``timezone`` and ``sync``.
        :return: the decoded JSON reply, e.g. ``{"status": true}``, or the
            ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when a required field is missing.

        .. versionadded:: 1.0.0
        """
        self._require(kwargs, self.MASTER_ROUTE_CREATE_FIELDS)
        return self._call_api(RECURRING_MASTER_ROUTES_V5, "post", {}, body=dict(kwargs))

    # ------------------------------------------------------ scheduled routes

    def is_route_schedule_copied(self, route_id):
        """Tell whether the scheduled route of a route has been copied.

        Sends ``GET /modules/api/v5.0/recurring-routes/scheduled-routes/is-copy/{route_id}``.

        :param route_id: ID of the route.
        :return: the decoded JSON reply, ``{"status": true}`` or
            ``{"status": false}``, or the ``{"errors": ...}`` dict on an API
            error.
        :raise ParamValueException: when ``route_id`` is empty.

        .. versionadded:: 1.0.0
        """
        return self._call_api(self._url(RECURRING_SCHEDULED_ROUTES_IS_COPY_V5, route_id, "route_id"), "get", {})

    def get_route_schedule_copies(self, **kwargs):
        """List the routes copied from the scheduled route of a route.

        Sends ``POST /modules/api/v5.0/recurring-routes/scheduled-routes/get-copies``
        with the keywords as the JSON body.

        :param kwargs: the body. Required: ``route_id``. Optional:
            ``schedule_id`` and ``route_date`` (``YYYY-MM-DD``).
        :return: the decoded JSON reply, with ``parent_route_id`` and
            ``scheduled_routes``, or the ``{"errors": ...}`` dict on an API
            error.
        :raise ParamValueException: when ``route_id`` is missing.

        .. versionadded:: 1.0.0
        """
        self._require(kwargs, self.ROUTE_SCHEDULE_COPIES_FIELDS)
        return self._call_api(RECURRING_SCHEDULED_ROUTES_GET_COPIES_V5, "post", {}, body=dict(kwargs))

    # ------------------------------------------------------- calendar (V4)

    def get_schedule_calendar(self, **kwargs):
        """Count the scheduled routes, orders and contacts per day (API V4).

        Sends ``GET /api/schedule_calendar_data.php`` on ``api.route4me.com``
        with the keywords as the query. A ``bool`` value is sent as ``1`` or
        ``0``.

        :param kwargs: query parameters: ``date_from_string`` and
            ``date_to_string`` (``YYYY-MM-DD``), ``member_id``,
            ``timezone_offset_minutes``, and the flags ``orders``, ``ab``
            (address book contacts) and ``routes_count``.
        :return: the decoded JSON reply, or the ``{"errors": ...}`` dict on an
            API error.

        .. versionadded:: 1.0.0
        """
        params = {name: int(value) if isinstance(value, bool) else value for name, value in kwargs.items()}
        return self._call_api(SCHEDULE_CALENDAR, "get", params)
