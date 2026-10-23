"""The :class:`Route` resource: get, update, resequence, rename, share, merge, export and delete routes."""

import warnings

from ._url import path_segment
from .api_endpoints import (
    ADDRESS_HOST,
    DUPLICATE_ROUTE,
    EXPORTER,
    EXPORTER_V5,
    GET_ACTIVITIES_HOST,
    MERGE_ROUTES_HOST,
    RENAME_ROUTE,
    RESEQUENCE_ROUTE,
    ROUTE_HOST,
    SHARE_ROUTE_HOST,
)
from .base import Base
from .config import UNSET
from .exceptions import APIException, ParamValueException


class Route(Base):
    """Routes: sequences of addresses visited by one vehicle and one driver.

    A route is a multi-sequence of addresses that need to be visited by a
    single vehicle and a single driver in a fixed time period. Use it as
    ``route4me.route``.

    Unless stated otherwise, a method returns the decoded JSON reply, or on an
    API error the ``{"errors": ...}`` dict from :meth:`APIException.to_dict
    <route4me.exceptions.APIException.to_dict>` instead of raising.
    """

    requirements = [
        "api_key",
        "route_id",
    ]

    def __init__(self, api):
        self.response = None
        self.params = {"api_key": api.key}
        Base.__init__(self, api)

    def get_route(self, **kwargs):
        """Get a route by ID.

        Sends ``GET /api.v4/route.php``. Each keyword goes through its setter
        (see :meth:`~route4me.base.Base.validate_params`) and is sent as a
        query parameter.

        :param kwargs: query parameters. Required: ``route_id``. Others include
            ``directions=1`` for driving directions, ``route_path_output``
            (a :data:`~route4me.constants.ROUTE_PATH_OUTPUT` value) for the
            path, and ``device_tracking_history=1`` for the tracking history.
        :return: the decoded JSON reply: the route, or the ``{"errors": ...}``
            dict on an API error.
        :raise ParamValueException: when ``route_id`` is missing, or a keyword
            is not a supported parameter or has an invalid value.
        """
        params = self.validated_params(**kwargs)
        params.update(kwargs)
        return self._call_api(ROUTE_HOST, "get", params, required=self.requirements)

    def get_route_tracking(self, **kwargs):
        """Get a route with its GPS tracking history.

        Sends ``GET /api.v4/route.php`` with ``device_tracking_history=1``.
        Each keyword goes through its setter, as in :meth:`get_route`.

        :param kwargs: query parameters. Required: ``route_id``.
        :return: the decoded JSON reply: the route, with ``tracking_history``,
            or the ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when ``route_id`` is missing, or a keyword
            is not a supported parameter or has an invalid value.
        """
        params = self.validated_params(**kwargs)
        params.update(kwargs)
        params["device_tracking_history"] = 1
        return self._call_api(ROUTE_HOST, "get", params, required=self.requirements)

    def get_routes(self, **kwargs):
        """List routes, a page at a time.

        Sends ``GET /api.v4/route.php``.

        :param kwargs: query parameters. Required: ``limit`` and ``offset``.
        :return: the decoded JSON reply: a list of routes, or the
            ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when ``limit`` or ``offset`` is missing.
        """
        kwargs.update({"api_key": self.params["api_key"]})
        return self._call_api(ROUTE_HOST, "get", kwargs, required=["limit", "offset"])

    def get_activities(self, **kwargs):
        """Get the activities recorded on a route, a page at a time.

        Sends ``GET /api/get_activities.php``.

        :param kwargs: query parameters. Required: ``route_id``, ``limit`` and
            ``offset``.
        :return: the decoded JSON reply: the activities, or the
            ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when a required parameter is missing.
        """
        kwargs.update({"api_key": self.params["api_key"]})
        return self._call_api(GET_ACTIVITIES_HOST, "get", kwargs, required=["route_id", "limit", "offset"])

    def duplicate_route(self, **kwargs):
        """Duplicate a route.

        Sends ``GET /actions/duplicate_route.php``.

        :param kwargs: query parameters. Required: ``route_id``, the route to
            copy.
        :return: the decoded JSON reply, which describes the new route, or the
            ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when ``route_id`` is missing.
        """
        kwargs.update({"api_key": self.params["api_key"]})
        return self._call_api(DUPLICATE_ROUTE, "get", kwargs, required=["route_id"])

    def delete_routes(self, **kwargs):
        """Delete several routes.

        Sends ``DELETE /api.v4/route.php`` with the route IDs, comma-separated,
        as ``route_id`` in the query.

        :param kwargs: query parameters. Required: ``route_id``, the IDs of the
            routes to delete as a list, e.g. ``route_id=[id_1, id_2]``, or one
            ID or a comma-separated string of IDs.
        :return: the decoded JSON reply, which lists the deleted route IDs, or
            the ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when ``route_id`` is missing.
        """
        if not self.check_required_params(kwargs, ["route_id"]):
            raise ParamValueException("params", "Params are not complete")
        route_ids = kwargs["route_id"]
        kwargs["route_id"] = route_ids if isinstance(route_ids, str) else ",".join(route_ids)
        kwargs["api_key"] = self.params["api_key"]
        return self._call_api(ROUTE_HOST, "delete", kwargs)

    def delete_route(self, **kwargs):
        """Delete one route.

        Sends ``DELETE /api.v4/route.php``.

        :param kwargs: query parameters. Required: ``route_id``.
        :return: the ``deleted`` value of the reply when it has one, otherwise
            the decoded JSON reply as is, or the ``{"errors": ...}`` dict on an
            API error.
        :raise ParamValueException: when ``route_id`` is missing.
        """
        kwargs.update({"api_key": self.params["api_key"]})
        if not self.check_required_params(kwargs, ["route_id"]):
            raise ParamValueException("params", "Params are not complete")
        try:
            self.response = self._request(ROUTE_HOST, kwargs, "delete")
            payload = self.response.json()
        except APIException as e:
            return e.to_dict()
        # The old handler was `except AttributeError: return response.errors`,
        # which raised AttributeError itself whenever the payload was a dict
        # without an `errors` attribute -- i.e. always. Return the payload
        # untouched when it is not the expected `{"deleted": ...}` envelope.
        if isinstance(payload, dict) and "deleted" in payload:
            return payload["deleted"]
        return payload

    def insert_address_into_route(self, addresses, route_id, *, timeout=UNSET):
        """Add addresses to an existing route.

        Sends ``PUT /api.v4/route.php`` with ``route_id`` in the query and
        ``addresses`` as the body.

        :param addresses: the body: ``{"addresses": [...]}``, each address a
            dict with at least ``address``, ``lat`` and ``lng``. An address
            with a ``sequence_no`` is placed at that position.
        :param route_id: ID of the route.
        :param timeout: read timeout for this call, in seconds, or a
            ``(connect, read)`` pair. Inserting into a long route can take
            longer than the 30-second default. Unset uses the client's timeout.
        :return: the decoded JSON reply: the updated route, or the
            ``{"errors": ...}`` dict on an API error.
        """
        params = {"route_id": route_id}
        return self._update_route(params, addresses, timeout=timeout)

    def move_addresses_from_route(self, addresses, route_id, *, timeout=UNSET):
        """Move existing destinations into a route, at the given positions.

        Sends ``PUT /api.v4/route.php`` with ``route_id`` in the query and
        ``addresses`` as the body -- the same request as
        :meth:`insert_address_into_route`.

        :param addresses: the body: ``{"addresses": [...]}``, each address a
            dict with its ``route_destination_id`` and new ``sequence_no``.
        :param route_id: ID of the route the destinations go to.
        :param timeout: read timeout for this call, in seconds, or a
            ``(connect, read)`` pair. Inserting into a long route can take
            longer than the 30-second default. Unset uses the client's timeout.
        :return: the decoded JSON reply: the updated route, or the
            ``{"errors": ...}`` dict on an API error.
        """
        params = {"route_id": route_id}
        return self._update_route(params, addresses, timeout=timeout)

    def update_route_parameters(self, data, route_id, *, timeout=UNSET):
        """Update the parameters of a route.

        Sends ``PUT /api.v4/route.php`` with ``route_id`` in the query and
        ``data`` as the body.

        :param data: the body, e.g. ``{"parameters": {"route_name": "Monday"}}``.
        :param route_id: ID of the route.
        :param timeout: read timeout for this call, in seconds, or a
            ``(connect, read)`` pair. Inserting into a long route can take
            longer than the 30-second default. Unset uses the client's timeout.
        :return: the decoded JSON reply: the updated route, or the
            ``{"errors": ...}`` dict on an API error.
        """
        params = {"route_id": route_id}
        return self._update_route(params, data, timeout=timeout)

    def update_route(self, data, route_id, *, timeout=UNSET, **params):
        """Update the fields of a route, or re-optimize it.

        Sends ``PUT /api.v4/route.php`` with ``route_id`` and the other
        keywords in the query and ``data`` as the body.

        The same request adds orders to a route (``addresses`` with an
        ``order_id`` each), re-optimizes it, or recomputes its directions::

            route4me.route.update_route({}, route_id, reoptimize=1, remaining=1)
            route4me.route.update_route({}, route_id, recompute_directions=1)

        :param data: the body: the route fields to change, e.g.
            ``{"parameters": {...}}`` or ``{"addresses": [...]}``; ``{}``
            for none.
        :param route_id: ID of the route.
        :param timeout: read timeout for this call, in seconds, or a
            ``(connect, read)`` pair. Inserting into a long route can take
            longer than the 30-second default. Unset uses the client's timeout.
        :param params: more query parameters: ``reoptimize``, ``1`` to
            re-optimize the route after the update; ``remaining``, ``1`` with
            ``reoptimize=1`` to re-optimize only the stops not visited yet;
            ``prioritize_by``, the attribute the remaining stops are ordered
            by; ``recompute_directions``, ``1`` to recompute the directions;
            and ``recompute_actual_distance``, ``1`` to recompute the actual
            distance.
        :return: the decoded JSON reply: the updated route, or the
            ``{"errors": ...}`` dict on an API error.

        .. versionchanged:: 1.0.0
           Takes the query parameters of the API as keywords, so the method
           also re-optimizes a route and recomputes its directions.
        """
        params["route_id"] = route_id
        return self._update_route(params, data, timeout=timeout)

    def rename_route(self, route_id, route_name):
        """Rename a route.

        Sends ``POST /actions/route/rename_route.php`` with ``format=json`` in
        the query and ``route_id`` and ``route_name`` as form fields.

        :param route_id: ID of the route.
        :param route_name: the new name.
        :return: the decoded JSON reply, or the ``{"errors": ...}`` dict on an
            API error.
        :raise ParamValueException: when ``route_id`` or ``route_name`` is
            empty.

        .. versionadded:: 1.0.0
        """
        missing = [name for name, value in (("route_id", route_id), ("route_name", route_name)) if not value]
        if missing:
            raise ParamValueException(", ".join(missing), "Missing required params")
        body = {"route_id": route_id, "route_name": route_name}
        return self._call_api(RENAME_ROUTE, "post", {"format": "json"}, body=body, body_key="data")

    def insert_address_into_route_optimal_position(self, **kwargs):
        """Insert addresses into a route, each at its optimal position.

        Sends ``PUT /api.v4/route.php`` with ``route_id`` in the query and the
        other keywords as the JSON body.

        :param kwargs: required: ``route_id``; ``addresses``, a list of address
            dicts; and ``optimal_position``, ``True`` to let the API choose the
            positions.
        :return: the decoded JSON reply: the updated route, or the
            ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when a required parameter is missing.
        """
        if self.check_required_params(kwargs, ["addresses", "route_id", "optimal_position"]):
            params = {"api_key": self.params["api_key"], "route_id": kwargs.pop("route_id")}
            try:
                self.response = self._request(ROUTE_HOST, params, "put", json=kwargs)
                return self.response.json()
            except APIException as e:
                return e.to_dict()
        else:
            raise ParamValueException("params", "Params are not complete")

    def get_route_path_points(self, **kwargs):
        """Get a route with the path points between its stops.

        Sends ``GET /api.v4/route.php``.

        :param kwargs: query parameters. Required: ``route_id`` and
            ``route_path_output``, a :data:`~route4me.constants.ROUTE_PATH_OUTPUT`
            value such as ``"Points"``.
        :return: the decoded JSON reply: the route, or the ``{"errors": ...}``
            dict on an API error.
        :raise ParamValueException: when a required parameter is missing.
        """
        kwargs.update({"api_key": self.params["api_key"]})
        return self._call_api(ROUTE_HOST, "get", kwargs, required=["route_path_output", "route_id"])

    def get_route_directions(self, **kwargs):
        """Get a route with its driving directions.

        Sends ``GET /api.v4/route.php``.

        :param kwargs: query parameters. Required: ``route_id`` and
            ``directions``, ``1`` to include the directions.
        :return: the decoded JSON reply: the route, with ``directions``, or the
            ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when a required parameter is missing.
        """
        kwargs.update({"api_key": self.params["api_key"]})
        return self._call_api(ROUTE_HOST, "get", kwargs, required=["directions", "route_id"])

    def share_route(self, **kwargs):
        """Share a route by email.

        Sends ``POST /actions/route/share_route.php`` with ``route_id`` and
        ``response_format`` in the query and the other keywords as the JSON
        body.

        :param kwargs: required: ``route_id``; ``response_format``, e.g.
            ``"json"``; and ``recipient_email``, the address to share with.
        :return: the decoded JSON reply, or the ``{"errors": ...}`` dict on an
            API error.
        :raise ParamValueException: when a required parameter is missing.
        """
        if self.check_required_params(kwargs, ["recipient_email", "route_id", "response_format"]):
            params = {
                "api_key": self.params["api_key"],
                "route_id": kwargs.pop("route_id"),
                "response_format": kwargs.pop("response_format"),
            }
            try:
                self.response = self._request(SHARE_ROUTE_HOST, params, "post", json=kwargs)
                return self.response.json()
            except APIException as e:
                return e.to_dict()
        else:
            raise ParamValueException("params", "Params are not complete")

    def resequence_route(self, **kwargs):
        """Change the position of stops in a route.

        Sends ``PUT /api.v4/route.php`` with ``route_id`` and
        ``route_destination_id`` in the query and the other keywords as the
        JSON body.

        :param kwargs: required: ``route_id``; ``route_destination_id``; and
            ``addresses``, a list of ``{"route_destination_id": ...,
            "sequence_no": ...}`` dicts giving the new positions.
        :return: the decoded JSON reply: the updated route, or the
            ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when a required parameter is missing.
        """
        if self.check_required_params(kwargs, ["addresses", "route_id", "route_destination_id"]):
            params = {
                "api_key": self.params["api_key"],
                "route_id": kwargs.pop("route_id"),
                "route_destination_id": kwargs.pop("route_destination_id"),
            }
            try:
                self.response = self._request(ROUTE_HOST, params, "put", json=kwargs)
                return self.response.json()
            except APIException as e:
                return e.to_dict()
        else:
            raise ParamValueException("params", "Params are not complete")

    def resequence_multiple_stops(self, route_id, addresses_data):
        """Change the position of several stops in a route.

        Sends ``PUT /api.v4/route.php`` with ``route_id`` in the query and
        ``addresses_data`` as the JSON body.

        :param route_id: ID of the route.
        :param addresses_data: the body: ``{"addresses": [...]}``, each address
            a dict with its ``route_destination_id`` and new ``sequence_no``.
        :return: the decoded JSON reply: the updated route, or the
            ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when ``addresses_data`` has no
            ``addresses``.
        """
        if not self.check_required_params(addresses_data, ["addresses"]):
            raise ParamValueException("params", "Params are not complete")
        params = {
            "api_key": self.params["api_key"],
            "route_id": route_id,
        }
        return self._call_api(ROUTE_HOST, "put", params, body=addresses_data)

    def merge_routes(self, **kwargs):
        """Merge several routes into one.

        Sends ``POST /actions/merge_routes.php`` with the keywords as form
        fields.

        :param kwargs: form fields. Required: ``route_ids``, the IDs of the
            routes to merge: a comma-separated string or a list of IDs.
        :return: the decoded JSON reply, or the ``{"errors": ...}`` dict on an
            API error.
        :raise ParamValueException: when ``route_ids`` is missing.

        .. versionchanged:: 1.0.0
           ``route_ids`` may be a list. It used to be form-encoded as one field
           per ID, which the API does not read.
        """
        if not self.check_required_params(kwargs, ["route_ids"]):
            raise ParamValueException("params", "Params are not complete")
        body = dict(kwargs)
        if not isinstance(body["route_ids"], str):
            body["route_ids"] = ",".join(str(route_id) for route_id in body["route_ids"])
        return self._call_api(MERGE_ROUTES_HOST, "post", self.params, body=body, body_key="data")

    def resequence_route_all(self, **kwargs):
        """Resequence all the stops of a route.

        Sends ``GET /api.v3/route/reoptimize_2.php``.

        :param kwargs: query parameters. Required: ``route_id``;
            ``disable_optimization``, ``0`` or ``1``; and ``optimize``, an
            :data:`~route4me.constants.OPTIMIZE` value such as ``"Distance"``.
        :return: the decoded JSON reply, or the ``{"errors": ...}`` dict on an
            API error.
        :raise ParamValueException: when a required parameter is missing.
        """
        kwargs.update({"api_key": self.params["api_key"]})
        return self._call_api(
            RESEQUENCE_ROUTE, "get", kwargs, required=["disable_optimization", "route_id", "optimize"]
        )

    def update_route_destination_custom_data(self, **kwargs):
        """Update a destination of a route, e.g. its custom data.

        Sends ``PUT /api.v4/address.php`` with ``route_id`` and
        ``route_destination_id`` in the query and the other keywords as the
        JSON body.

        :param kwargs: required: ``route_id`` and ``route_destination_id``. The
            other keywords are the fields to change, e.g.
            ``custom_fields={"color": "red"}``.
        :return: the decoded JSON reply: the updated destination, or the
            ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when a required parameter is missing.
        """
        if not self.check_required_params(kwargs, ["route_id", "route_destination_id"]):
            raise ParamValueException("params", "Params are not complete")
        params = {
            "api_key": self.params["api_key"],
            "route_id": kwargs.pop("route_id"),
            "route_destination_id": kwargs.pop("route_destination_id"),
        }
        return self._call_api(ADDRESS_HOST, "put", params, body=kwargs)

    def export_route(self, route_id, output_format="csv"):
        """Export a route.

        Sends ``POST /actions/route/export_current_route.php`` with
        ``route_id`` and ``strExportFormat`` as form fields.

        :param route_id: ID of the route.
        :param output_format: export format, ``"csv"`` by default.
        :return: the raw response body (``bytes``).
        :raise APIException: when the API answers outside the 200-399 range.

        .. deprecated:: 1.0.0
           ``/actions/route/export_current_route.php`` returns 404. Use
           :meth:`export_route_v5`.
        """
        warnings.warn("export_route is deprecated. Please use export_route_v5", DeprecationWarning, stacklevel=2)
        data = {"route_id": route_id, "strExportFormat": output_format}
        self.response = self._request(EXPORTER, {}, "post", data=data)
        return self.response.content

    def _update_route(self, params, data, *, timeout=UNSET):
        """Send ``PUT /api.v4/route.php`` with ``data`` as the JSON body.

        :param params: query parameters, including ``route_id``.
        :param data: the request body.
        :param timeout: read timeout for this call; unset uses the client's.
        :return: the decoded JSON reply, or the ``{"errors": ...}`` dict on an
            API error.

        .. versionchanged:: 1.0.0
           The body is JSON again. Since 0.1.6.0 it had been sent as form data,
           which the API cannot read for nested addresses or parameters (#19).
        """
        params.update({"api_key": self.api.key})
        try:
            response = self._request(ROUTE_HOST, params, "put", json=data, timeout=timeout)
            return response.json()
        except APIException as e:
            return e.to_dict()

    def export_route_v5(self, route_id, output_format="csv", all_custom_fields=True, columns=None):
        """Export a route with API V5.

        Sends ``POST /modules/api/v5.0/route-export/{route_id}/export`` to
        ``wh.route4me.com`` with ``format``, ``all_custom_fields`` and
        ``columns`` as the JSON body.

        :param route_id: ID of the route.
        :param output_format: export format, ``"csv"`` by default.
        :param all_custom_fields: include every custom field.
        :param columns: the columns to export; ``None`` leaves the choice to
            the API.
        :return: the raw response body (``bytes``), or the ``{"errors": ...}``
            dict on an API error.
        :raise ParamValueException: when ``route_id`` is empty.

        .. versionchanged:: 1.0.0
           The body is JSON, as the API documents. As form data,
           ``all_custom_fields=True`` arrived as the string ``"True"``.
        """
        url = EXPORTER_V5.format(route_id=path_segment(route_id, "route_id"))
        params = {
            "api_key": self.params["api_key"],
        }
        data = {"all_custom_fields": all_custom_fields, "format": output_format}
        if columns is not None:
            data["columns"] = columns
        try:
            self.response = self._request(url, params, "post", json=data)
            return self.response.content
        except APIException as e:
            return e.to_dict()
