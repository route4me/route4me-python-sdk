"""The :class:`Address` resource: the stops of routes and optimizations, their notes, and geocoding.

It also moves, deletes and marks the stops of routes.
"""

import json
import logging
import time

import requests

from ._resilience import backoff_delay
from .api_endpoints import (
    ADD_ROUTE_NOTES_HOST,
    ADDRESS_HOST,
    BATCH_GEOCODER,
    DELETE_ROUTE_DESTINATION,
    MARK_ADDRESS_DEPARTED,
    MARK_ADDRESS_VISITED,
    MOVE_ROUTE_DESTINATION,
    SINGLE_GEOCODER,
)
from .base import Base
from .exceptions import APIException, ParamValueException

logger = logging.getLogger(__name__)

#: Attempts (including the first) when geocoding a single address.
MAX_GEOCODE_ATTEMPTS = 6

#: Backoff base for geocode retries, in seconds. Larger than the transport's
#: 0.2s because a geocoding failure usually means the geocoder is saturated
#: rather than momentarily unreachable.
GEOCODE_RETRY_INITIAL_DELAY = 0.5


class Address(Base):
    """Addresses: the destinations of routes and optimization problems.

    An address is a destination in a route or optimization problem. An address
    can be a depot, i.e. a departure point. An address belongs to only one
    route and one optimization problem, except for depots: one depot can be
    part of many routes in a VRP (multi-route) solution. Use it as
    ``route4me.address``.

    Unless stated otherwise, a method returns the decoded JSON reply, or on an
    API error the ``{"errors": ...}`` dict from :meth:`APIException.to_dict
    <route4me.exceptions.APIException.to_dict>` instead of raising.
    """

    REQUIRED_FIELDS = [
        "lat",
        "lng",
    ]

    def __init__(self, api):
        """Create the resource with an empty address list.

        :param api: the :class:`~route4me.api.Route4Me` client.
        """
        self.addresses = []
        Base.__init__(self, api)

    def get_route_id(self):
        """Return the route ID of the last response.

        :return: the ``route_id`` of the last decoded response.
        """
        return self._last_payload()["route_id"]

    def get_route_destination_id(self):
        """Return the route destination ID of the last response.

        :return: the ``route_destination_id`` of the last decoded response.
        """
        return self._last_payload()["route_destination_id"]

    def _last_payload(self):
        """Return the decoded body of the last response this resource received.

        :return: the decoded JSON of :attr:`response`, or :attr:`response`
            itself when it is already decoded.
        :raise ParamValueException: when no request has been made yet.
        """
        if self.response is None:
            raise ParamValueException("response", "No request has been made yet")
        return self.response.json() if hasattr(self.response, "json") else self.response

    def get_addresses(self):
        """Return the addresses of the optimization being built.

        These are the addresses added with :meth:`add_address`, or those stored
        by :meth:`Route4Me.get_optimization
        <route4me.api.Route4Me.get_optimization>`.

        :return: the list of address dicts.
        """
        return self.addresses

    def add_address(self, **kwargs):
        """Add an address to the optimization being built.

        The address is appended to the list that :meth:`get_addresses`
        returns, which becomes the ``addresses`` of the request that
        :meth:`Route4Me.run_optimization <route4me.api.Route4Me.run_optimization>`
        sends.

        :param kwargs: the address fields, e.g. ``address``, ``lat`` and
            ``lng``. Required: ``lat`` and ``lng``, or an ``order_id``, or a
            ``contact_id``.
        :raise ParamValueException: when none of these is given.
        """
        if (
            self.check_required_params(kwargs, self.REQUIRED_FIELDS)
            or self.check_required_params(kwargs, ["order_id"])
            or self.check_required_params(kwargs, ["contact_id"])
        ):
            self.addresses.append(kwargs)
            self.api.optimization.data["addresses"] = self.addresses
        else:
            raise ParamValueException("addresses", "Params are not complete")

    def batch_fix_geocodes(self, addresses):
        """Geocode several addresses in one request and store the coordinates.

        Sends the ``address`` of every item, separated by ``||``, with
        :meth:`get_batch_geocodes` (``POST /api/geocoder.php``). Each result is
        matched back to its input address, which gets the result's ``lat`` and
        ``lng``.

        :param addresses: a list of dicts, each with an ``address`` string.
            Matched dicts are updated in place.
        :return: ``(geocoding_error, addresses)``: the results that could not
            be matched to an input address, and the input list. When the reply
            is not JSON, every address is an error.
        """
        geocoding_error = []
        params = {
            "format": "json",
        }
        addresses_map = {x["address"].replace("/", " - "): x for x in addresses}
        data = {"addresses": "||".join([x["address"] for x in addresses])}
        try:
            json_data = self.get_batch_geocodes(params, data)
        except json.decoder.JSONDecodeError:
            logger.warning("Error Geocoding some of the Addresses. Please check the addresses and try again.")
            # Returns (geocoding_error, addresses), matching the success path at
            # the end of this method. This used to return `addresses, []` --
            # the two slots swapped -- so a caller unpacking
            # `errors, addresses = batch_fix_geocodes(...)` silently got its
            # addresses in the error variable and an empty list of addresses.
            # The whole batch failed, so every address is an error.
            return list(addresses), addresses
        if not isinstance(json_data, list):
            # An API error comes back as the {"errors": ...} dict: nothing was geocoded.
            return list(addresses), addresses
        for address in json_data:
            original_address = addresses_map.get(address.get("original")) if isinstance(address, dict) else None
            if original_address is None or "lat" not in address or "lng" not in address:
                geocoding_error.append(address)
                continue
            original_address.update({"lat": address["lat"], "lng": address["lng"]})
        return geocoding_error, addresses

    def get_geocode(self, params):
        """Geocode one address.

        Sends ``GET /api/address.php``.

        :param params: query parameters, e.g. ``{"format": "json", "address":
            "754 5th Ave New York, NY 10019"}``.
        :return: the decoded JSON reply, or the ``{"errors": ...}`` dict on an
            API error.
        """
        try:
            self.response = self._request(SINGLE_GEOCODER, params, "get")
            return self.response.json()
        except APIException as e:
            return e.to_dict()

    def get_batch_geocodes(self, params, data):
        """Geocode several addresses.

        Sends ``POST /api/geocoder.php`` with ``data`` as form fields.

        :param params: query parameters, e.g. ``{"format": "json"}``.
        :param data: form fields: ``addresses``, the addresses separated by
            ``||``.
        :return: the decoded JSON reply, or the ``{"errors": ...}`` dict on an
            API error.
        """
        try:
            self.response = self._request(BATCH_GEOCODER, params, "post", data=data)
            return self.response.json()
        except APIException as e:
            return e.to_dict()

    def fix_geocode(self, address, max_attempts=MAX_GEOCODE_ATTEMPTS):
        """Geocode one address, retrying transient failures.

        Calls :meth:`get_geocode` with the item's ``address`` and copies the
        ``lat`` and ``lng`` of the first result into the dict. A connection
        error is retried with exponential backoff, up to ``max_attempts``
        attempts in all. An API error or a reply without coordinates is a
        failure and is not retried.

        :param address: a dict with an ``address`` string, updated in place.
        :param max_attempts: attempts in all, including the first.
        :return: ``(geocoding_error, address)`` -- ``geocoding_error`` is
            ``None`` on success, or the address itself when every attempt failed.

        .. versionchanged:: 1.0.0
           The geocoder answers with a list of results; only the first one's
           coordinates are copied. The whole reply used to be merged into the
           dict, which raised ``ValueError``, corrupted the address, or merged
           an API error and reported success.

           Backoff now comes from :func:`route4me._resilience.backoff_delay`,
           the same exponential-with-jitter policy the transport uses. The
           previous loop slept ``random.randrange(1, 5) * 0.5`` -- uniform, not
           exponential, so it did not back off under sustained failure.
        """
        params = {"format": "json", "address": address.get("address")}
        for attempt in range(1, max_attempts + 1):
            try:
                json_data = self.get_geocode(params)
            except requests.exceptions.ConnectionError:
                if attempt >= max_attempts:
                    return address, address
                time.sleep(backoff_delay(attempt, GEOCODE_RETRY_INITIAL_DELAY))
                continue
            result = json_data[0] if isinstance(json_data, list) and json_data else json_data
            if not isinstance(result, dict) or "lat" not in result or "lng" not in result:
                return address, address
            address.update({"lat": result["lat"], "lng": result["lng"]})
            return None, address
        # Unreachable: the loop either returns or exhausts max_attempts above.
        return address, address

    def request_address(self, params):
        """Send ``GET /api.v4/address.php``.

        :param params: query parameters, e.g. ``route_id`` and
            ``route_destination_id``. The caller's dict is not changed.
        :return: the :class:`requests.Response`, or the ``{"errors": ...}``
            dict on an API error.
        """
        params = dict(params, api_key=self.api.key)
        try:
            self.response = self._request(ADDRESS_HOST, params, "get")
            return self.response
        except APIException as e:
            return e.to_dict()

    def get_address(self, route_id, route_destination_id):
        """Get one destination of a route.

        Sends ``GET /api.v4/address.php``.

        :param route_id: ID of the route.
        :param route_destination_id: ID of the destination in that route.
        :return: the decoded JSON reply: the address, or the
            ``{"errors": ...}`` dict on an API error.
        """
        params = {"route_id": route_id, "route_destination_id": route_destination_id}
        response = self.request_address(params)
        return response if isinstance(response, dict) else response.json()

    def get_address_notes(self, route_id, route_destination_id):
        """Get one destination of a route, with its notes.

        Sends ``GET /api.v4/address.php`` with ``notes=True``.

        :param route_id: ID of the route.
        :param route_destination_id: ID of the destination in that route.
        :return: the decoded JSON reply: the address, with ``notes``, or the
            ``{"errors": ...}`` dict on an API error.
        """
        params = {
            "route_id": route_id,
            "route_destination_id": route_destination_id,
            "notes": True,
        }
        response = self.request_address(params)
        return response if isinstance(response, dict) else response.json()

    def update_address(self, data, route_id, route_destination_id):
        """Update one destination of a route.

        Sends ``PUT /api.v4/address.php`` with ``data`` as the JSON body.

        :param data: the address fields to change, e.g. ``{"alias": "Gate 2"}``.
        :param route_id: ID of the route.
        :param route_destination_id: ID of the destination in that route.
        :return: the decoded JSON reply: the updated address, or the
            ``{"errors": ...}`` dict on an API error.
        """
        params = {"route_id": route_id, "route_destination_id": route_destination_id}
        params.update({"api_key": self.api.key})
        try:
            response = self._request(ADDRESS_HOST, params, "put", json=data)
            return response.json()
        except APIException as e:
            return e.to_dict()

    def delete_address_from_route(self, route_id, route_destination_id):
        """Remove one destination from a route.

        Sends ``DELETE /api.v4/address.php``.

        :param route_id: ID of the route.
        :param route_destination_id: ID of the destination to remove.
        :return: the decoded JSON reply, or the ``{"errors": ...}`` dict on an
            API error.
        """
        params = {"route_id": route_id, "route_destination_id": route_destination_id}
        params.update({"api_key": self.api.key})
        try:
            response = self._request(ADDRESS_HOST, params, "delete")
            return response.json()
        except APIException as e:
            return e.to_dict()

    def move_destination_to_route(self, to_route_id, route_destination_id, after_destination_id=None):
        """Move a destination to another route.

        Sends ``POST /actions/route/move_route_destination.php`` with
        ``to_route_id``, ``route_destination_id`` and ``after_destination_id``
        as form fields.

        :param to_route_id: ID of the route the destination moves to.
        :param route_destination_id: ID of the destination to move.
        :param after_destination_id: ID of the destination of ``to_route_id``
            after which the moved one is inserted. ``None`` (the default)
            leaves the position to the API.
        :return: the decoded JSON reply, with ``success``, or the
            ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when ``to_route_id`` or
            ``route_destination_id`` is empty.

        .. versionadded:: 1.0.0
        """
        required = (("to_route_id", to_route_id), ("route_destination_id", route_destination_id))
        missing = [name for name, value in required if value is None or value == ""]
        if missing:
            raise ParamValueException(", ".join(missing), "Missing required params")
        data = {"to_route_id": to_route_id, "route_destination_id": route_destination_id}
        if after_destination_id is not None:
            data["after_destination_id"] = after_destination_id
        return self._call_api(MOVE_ROUTE_DESTINATION, "post", {}, body=data, body_key="data")

    def delete_route_destinations(self, route_destination_ids):
        """Delete one or more destinations from their routes.

        Sends ``POST /actions/route/delete_route_destination.php`` with
        ``format=json`` in the query and ``route_destination_ids``,
        comma-separated, as a form field.

        :param route_destination_ids: the IDs of the destinations: a list, or
            one ID or a comma-separated string of IDs.
        :return: the decoded JSON reply, or the ``{"errors": ...}`` dict on an
            API error.
        :raise ParamValueException: when no ID is given.

        .. versionadded:: 1.0.0
        """
        if isinstance(route_destination_ids, (str, int)):
            route_destination_ids = [route_destination_ids]
        ids = ",".join(str(destination_id) for destination_id in route_destination_ids)
        if not ids:
            raise ParamValueException("route_destination_ids", "Missing required params")
        # The endpoint reads route_destination_id, comma-separated; it rejects
        # route_destination_ids (checked live on 2026-10-22).
        data = {"route_destination_id": ids}
        return self._call_api(DELETE_ROUTE_DESTINATION, "post", {"format": "json"}, body=data, body_key="data")

    def mark_address_departed(self, route_id, address_id, is_departed=True, **kwargs):
        """Mark a destination of a route as departed, or clear the mark.

        Sends ``GET /api/route/mark_address_departed.php`` with the arguments
        in the query.

        :param route_id: ID of the route.
        :param address_id: ID of the destination in that route.
        :param is_departed: ``True`` (the default) to mark it, ``False`` to
            clear the mark. Sent as ``1`` or ``0``.
        :param kwargs: optional query parameters: ``member_id``, the member
            who departed; ``utc_time``, when, as a Unix timestamp; and ``lat``
            and ``lng``, where.
        :return: the decoded JSON reply, with ``status``, or the
            ``{"errors": ...}`` dict on an API error.

        .. versionadded:: 1.0.0
        """
        params = dict(kwargs, route_id=route_id, address_id=address_id, is_departed=int(bool(is_departed)))
        return self._call_api(MARK_ADDRESS_DEPARTED, "get", params)

    def mark_address_visited(self, route_id, address_id, is_visited=True, **kwargs):
        """Mark a destination of a route as visited, or clear the mark.

        Sends ``PUT /api/route/mark_address_visited.php`` with the arguments
        in the query.

        :param route_id: ID of the route.
        :param address_id: ID of the destination in that route.
        :param is_visited: ``True`` (the default) to mark it, ``False`` to
            clear the mark. Sent as ``1`` or ``0``.
        :param kwargs: optional query parameters: ``member_id``, the member
            who visited; ``utc_time``, when, as a Unix timestamp; and ``lat``
            and ``lng``, where.
        :return: the decoded JSON reply, or the ``{"errors": ...}`` dict on an
            API error.

        .. versionadded:: 1.0.0
        """
        params = dict(kwargs, route_id=route_id, address_id=address_id, is_visited=int(bool(is_visited)))
        return self._call_api(MARK_ADDRESS_VISITED, "put", params)

    def add_address_notes(self, note, **kwargs):
        """Add a note to one destination of a route.

        Sends ``POST /actions/addRouteNotes.php`` with the keywords, except
        ``activity_type``, in the query, and ``strUpdateType`` and
        ``strNoteContents`` as form fields.

        :param note: the text of the note.
        :param kwargs: required: ``route_id`` and ``address_id``, the route
            destination ID. ``activity_type`` is sent as ``strUpdateType``.
        :return: the decoded JSON reply, or the ``{"errors": ...}`` dict on an
            API error.
        :raise ParamValueException: when ``route_id`` or ``address_id`` is
            missing.
        """
        if not self.check_required_params(kwargs, ["address_id", "route_id"]):
            raise ParamValueException("params", "Params are not complete")
        data = {"strNoteContents": note}
        if "activity_type" in kwargs:
            data["strUpdateType"] = kwargs.pop("activity_type")
        kwargs["api_key"] = self.params["api_key"]
        return self._call_api(ADD_ROUTE_NOTES_HOST, "post", kwargs, body=data, body_key="data")

    def geocode(self, **kwargs):
        """Geocode several addresses in one request.

        Sends ``POST /api/geocoder.php`` with ``addresses`` as a form field in
        the body and the other keywords in the query.

        :param kwargs: required: ``addresses``, the addresses separated by
            ``||``. ``format`` is the response format, ``"csv"`` by default.
        :return: the raw response body (``bytes``), or the ``{"errors": ...}``
            dict on an API error.
        :raise ParamValueException: when ``addresses`` is missing.
        """
        if "format" not in kwargs:
            kwargs.update({"format": "csv"})
        kwargs.update(
            {
                "api_key": self.params["api_key"],
            }
        )
        if self.check_required_params(
            kwargs,
            [
                "addresses",
            ],
        ):
            body = {"addresses": kwargs.pop("addresses")}
            try:
                response = self._request(BATCH_GEOCODER, kwargs, "post", data=body)
                return response.content
            except APIException as e:
                return e.to_dict()
        else:
            raise ParamValueException("params", "Params are not complete")
