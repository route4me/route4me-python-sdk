"""The :class:`RoutesV5` resource (API V5): list, search and delete routes, and read and write their custom data."""

from ._url import path_segment
from .api_endpoints import (
    ROUTES_CUSTOM_DATA_BULK_V5,
    ROUTES_CUSTOM_DATA_KEYS_V5,
    ROUTES_DATATABLE_CONFIG_V5,
    ROUTES_DATATABLE_V5,
    ROUTES_DELETE_V5,
    ROUTES_LIST_V5,
    ROUTES_LOOKUP_FOR_NEW_DESTINATION_V5,
    ROUTES_V5,
    ROUTES_V5_1,
)
from .base import Base
from .exceptions import ParamValueException


class RoutesV5(Base):
    """Routes, through API V5.

    Use it as ``route4me.routes_v5``. It mirrors ``RouteManagerV5`` and
    ``RouteCustomDataManagerV5`` of the C# SDK. Every method sends a request to
    ``/modules/api/v5.0/routes...`` on ``wh.route4me.com`` (``v5.1`` for
    :meth:`get_routes_by_filter`), with the API key as a bearer token. The
    API V4 routes are in :class:`~route4me.route.Route`.

    Unless stated otherwise, a method returns the decoded JSON reply, or on an
    API error the ``{"errors": ...}`` dict from :meth:`APIException.to_dict
    <route4me.exceptions.APIException.to_dict>` instead of raising.

    .. versionadded:: 1.0.0
    """

    def __init__(self, api):
        """Create the resource.

        :param api: the :class:`~route4me.api.Route4Me` client.
        """
        Base.__init__(self, api)

    @staticmethod
    def _custom_data_url(route_id):
        """Build the custom-data URL of a route, with ``route_id`` encoded as one path segment.

        :param route_id: ID of the route.
        :return: the absolute URL.
        :raise ParamValueException: when ``route_id`` is empty.
        """
        return f"{ROUTES_V5}/{path_segment(route_id, 'route_id')}/custom-data"

    def get_routes(self, **kwargs):
        """List routes, a page at a time, with filters and sorting.

        Sends ``POST /modules/api/v5.0/routes`` with the keywords as the JSON
        body.

        :param kwargs: the body, all optional: ``filters``, a dict such as
            ``{"schedule_date": ["2026-10-01", "2026-10-31"]}`` or
            ``{"route_id": [...]}``; ``search_query``; ``query``; ``order_by``,
            a list of ``[field, "asc"]`` or ``[field, "desc"]`` pairs;
            ``page``; ``per_page``; ``timezone``, an IANA name;
            ``group_by``; ``fields``; ``exist_fields``; and ``exclude_ids``.
        :return: the decoded JSON reply: the routes in ``data``, with
            ``links`` and ``meta``, or the ``{"errors": ...}`` dict on an API
            error.

        .. versionadded:: 1.0.0
        """
        return self._call_api(ROUTES_V5, "post", {}, body=kwargs)

    def get_routes_list(self, **kwargs):
        """List routes, a page at a time, with filters, sorting and grouping.

        Sends ``POST /modules/api/v5.0/routes/list`` with the keywords as the
        JSON body.

        :param kwargs: the body, all optional, as for :meth:`get_routes`:
            ``filters``, ``search_query``, ``query``, ``order_by``, ``page``,
            ``per_page`` (at most 500), ``timezone``, ``group_by`` (e.g.
            ``"start_date"``, ``"vehicle"`` or ``"status"``), ``fields``,
            ``exist_fields`` and ``exclude_ids``.
        :return: the decoded JSON reply: the routes in ``data``, with
            ``links`` and ``meta``, or the ``{"errors": ...}`` dict on an API
            error.

        .. versionadded:: 1.0.0
        """
        return self._call_api(ROUTES_LIST_V5, "post", {}, body=kwargs)

    def get_routes_by_filter(self, **kwargs):
        """Search routes with filters, for example by schedule or creation date.

        Sends ``POST /modules/api/v5.1/routes`` (API 5.1) with the keywords as
        the JSON body.

        :param kwargs: the body, all optional: ``filters``, a dict such as
            ``{"schedule_date": ["2026-10-01", "2026-10-31"]}`` or
            ``{"created_date": [...]}``; ``query`` or ``search_query``;
            ``order_by``, e.g. ``[["route_created_unix", "desc"]]``; ``page``;
            ``per_page``; ``timezone``, an IANA name; and ``directions`` and
            ``notes``, ``True`` to include them.
        :return: the decoded JSON reply: the routes in ``data``, with
            ``links`` and ``meta``, or the ``{"errors": ...}`` dict on an API
            error.

        .. versionadded:: 1.0.0
        """
        return self._call_api(ROUTES_V5_1, "post", {}, body=kwargs)

    def delete_routes(self, **kwargs):
        """Delete the routes that match the filters.

        Sends ``DELETE /modules/api/v5.0/routes/delete`` with the keywords as
        the JSON body.

        :param kwargs: the body. Required: ``filters``, a dict such as
            ``{"route_id": [id_1, id_2]}``, and ``signature``, the request
            signature the API verifies. Optional: ``exclude_ids``, the IDs to
            keep, and the other filtering keys of :meth:`get_routes_list`.
        :return: the decoded JSON reply, with ``status``, ``removed`` and
            ``async``, or the ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when ``filters`` or ``signature`` is
            missing.

        .. versionadded:: 1.0.0
        """
        missing = self._missing(kwargs, ["filters", "signature"])
        if missing:
            raise ParamValueException(", ".join(missing), "Missing required params")
        return self._call_api(ROUTES_DELETE_V5, "delete", {}, body=kwargs)

    def get_route_datatable(self, **kwargs):
        """List routes as rows of the route data table, with filters and sorting.

        Sends ``POST /modules/api/v5.0/routes/datatable`` with the keywords as
        the JSON body. It mirrors C# ``GetRouteDatatableWithElasticSearch``;
        :meth:`get_route_data_table_config` describes the columns.

        :param kwargs: the body, all optional: ``filters``, a dict such as
            ``{"schedule_date": ["2026-10-01", "2026-10-31"]}``, ``route_id``,
            ``vehicle_ids``, ``member_ids`` or ``route_status``;
            ``search_query``; ``order_by``, a list of ``[field, direction]``
            pairs; ``page``; ``per_page``; and ``timezone``.
        :return: the decoded JSON reply: the routes, or the ``{"errors": ...}``
            dict on an API error.

        .. versionadded:: 1.0.0
        """
        return self._call_api(ROUTES_DATATABLE_V5, "post", {}, body=kwargs)

    def get_route_data_table_config(self):
        """Get the configuration of the route data table: its columns and filters.

        Sends ``GET /modules/api/v5.0/routes/datatable/config``.

        :return: the decoded JSON reply, or the ``{"errors": ...}`` dict on an
            API error.

        .. versionadded:: 1.0.0
        """
        return self._call_api(ROUTES_DATATABLE_CONFIG_V5, "get", {})

    def dynamic_insert_route_addresses(self, **kwargs):
        """Find the routes, and the positions in them, best suited to take a new stop.

        Sends ``POST /modules/api/v5.0/routes/lookup-for-new-destination``
        with the keywords as the JSON body. Nothing is changed: the reply lists
        the candidate insertions with their added time and distance.

        :param kwargs: the body. Required: ``lat`` and ``lng``, the location of
            the new stop. Optional: ``scheduled_for``, a ``YYYY-MM-DD`` date;
            ``route_ids``; ``facility_ids``; ``filters``; ``query``;
            ``search_query``; ``insert_mode``; ``recommend_by``;
            ``lookup_results_limit``; ``max_increase_percent_allowed``; and
            ``time_window_start``, ``time_window_end``,
            ``time_window_start_2`` and ``time_window_end_2``, in seconds.
        :return: the decoded JSON reply: a list of the matched routes, or the
            ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when ``lat`` or ``lng`` is missing.

        .. versionadded:: 1.0.0
        """
        missing = self._missing(kwargs, ["lat", "lng"])
        if missing:
            raise ParamValueException(", ".join(missing), "Missing required params")
        return self._call_api(ROUTES_LOOKUP_FOR_NEW_DESTINATION_V5, "post", {}, body=kwargs)

    def get_route_custom_data(self, route_id):
        """Get the custom data of a route.

        Sends ``GET /modules/api/v5.0/routes/{route_id}/custom-data``.

        :param route_id: ID of the route.
        :return: the decoded JSON reply: the custom data, a dict of strings, or
            the ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when ``route_id`` is empty.

        .. versionadded:: 1.0.0
        """
        return self._call_api(self._custom_data_url(route_id), "get", {})

    def update_route_custom_data(self, route_id, custom_data):
        """Replace the custom data of a route.

        Sends ``PUT /modules/api/v5.0/routes/{route_id}/custom-data`` with
        ``custom_data`` as the JSON body. The whole custom data is replaced:
        keys left out are removed, and ``{}`` removes them all.

        :param route_id: ID of the route.
        :param custom_data: the new custom data, a dict of strings, e.g.
            ``{"priority": "high"}``.
        :return: the decoded JSON reply: the saved custom data, or the
            ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when ``route_id`` is empty.

        .. versionadded:: 1.0.0
        """
        return self._call_api(self._custom_data_url(route_id), "put", {}, body=dict(custom_data))

    def get_bulk_route_custom_data(self, route_ids):
        """Get the custom data of several routes.

        Sends ``POST /modules/api/v5.0/routes/custom-data/bulk`` with
        ``route_ids`` as the JSON body.

        :param route_ids: the IDs of the routes, a list; one ID may be given
            as a string.
        :return: the decoded JSON reply: the custom data of each route in
            ``data``, or the ``{"errors": ...}`` dict on an API error.

        .. versionadded:: 1.0.0
        """
        ids = [route_ids] if isinstance(route_ids, str) else list(route_ids)
        return self._call_api(ROUTES_CUSTOM_DATA_BULK_V5, "post", {}, body={"route_ids": ids})

    def get_custom_data_keys(self):
        """List the custom data keys used across the routes of the organization.

        Sends ``GET /modules/api/v5.0/routes/custom-data/keys``.

        :return: the decoded JSON reply: a list of key names, or the
            ``{"errors": ...}`` dict on an API error.

        .. versionadded:: 1.0.0
        """
        return self._call_api(ROUTES_CUSTOM_DATA_KEYS_V5, "get", {})
