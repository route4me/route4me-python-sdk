"""The :class:`RouteDestinationsV5` resource (API V5): list, get and sequence route destinations."""

from ._url import path_segment
from .api_endpoints import (
    ROUTE_DESTINATIONS_BY_ORDER_V5,
    ROUTE_DESTINATIONS_COLUMNS_V5,
    ROUTE_DESTINATIONS_LIST_FIELDS_V5,
    ROUTE_DESTINATIONS_LIST_V5,
    ROUTE_DESTINATIONS_SEQUENCE_V5,
    ROUTE_DESTINATIONS_SORTING_V5,
    ROUTE_DESTINATIONS_V5,
)
from .base import Base
from .exceptions import ParamValueException


def _required(value, name):
    """Return ``value``, or raise when a required value is missing.

    :param value: the value given.
    :param name: the parameter name reported in the error.
    :return: ``value``, unchanged.
    :raise ParamValueException: when ``value`` is ``None`` or an empty string.
    """
    if value is None or (isinstance(value, str) and not value.strip()):
        raise ParamValueException(name, "Missing required params")
    return value


class RouteDestinationsV5(Base):
    """Route destinations, the stops of routes, through API V5.

    Use it as ``route4me.route_destinations_v5``. It mirrors
    ``RouteDestinationsManagerV5`` of the C# SDK. Every method sends a request
    to ``/modules/api/v5.0/route-destinations...`` on ``wh.route4me.com``, with
    the API key as a bearer token. The API V4 destinations are in
    :class:`~route4me.address.Address`.

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

    def get_destinations_list(self, **kwargs):
        """List route destinations, a page at a time, with filters and sorting.

        Sends ``POST /modules/api/v5.0/route-destinations/list`` with the
        keywords as the JSON body.

        :param kwargs: the body. Required: ``filters``, a dict such as
            ``{"route_id": ["..."]}``. Optional: ``not_filters``,
            ``order_by``, ``page``, ``per_page``, ``group_by``, ``timezone``,
            ``fields`` and ``route``.
        :return: the decoded JSON reply: ``items``, ``current_page_index`` and
            ``total_items_count``, or the ``{"errors": ...}`` dict on an API
            error.
        :raise ParamValueException: when ``filters`` is missing.

        .. versionadded:: 1.0.0
        """
        missing = self._missing(kwargs, ["filters"])
        if missing:
            raise ParamValueException(", ".join(missing), "Missing required params")
        return self._call_api(ROUTE_DESTINATIONS_LIST_V5, "post", {}, body=kwargs)

    def get_destination_fields(self):
        """List the destination fields that can be filtered and sorted on.

        Sends ``GET /modules/api/v5.0/route-destinations/list/fields``.

        :return: the decoded JSON reply, with ``fields``, or the
            ``{"errors": ...}`` dict on an API error.

        .. versionadded:: 1.0.0
        """
        return self._call_api(ROUTE_DESTINATIONS_LIST_FIELDS_V5, "get", {})

    def get_destination_columns(self, columns_configurator_key):
        """Get the destination columns and their saved order for one column set.

        Sends ``GET /modules/api/v5.0/route-destinations/columns`` with
        ``columns_configurator_key`` in the query.

        :param columns_configurator_key: the key of the saved column set.
        :return: the decoded JSON reply: ``categories``, ``order`` and
            ``default_order``, or the ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when ``columns_configurator_key`` is empty.

        .. versionadded:: 1.0.0
        """
        params = {"columns_configurator_key": _required(columns_configurator_key, "columns_configurator_key")}
        return self._call_api(ROUTE_DESTINATIONS_COLUMNS_V5, "get", params)

    def edit_destination_columns(self, **kwargs):
        """Save the order of the destination columns for one column set.

        Sends ``PUT /modules/api/v5.0/route-destinations/columns`` with the
        keywords as the JSON body.

        :param kwargs: the body. Required: ``columns_configurator_key``, the
            key of the column set, and ``order``, the column names in display
            order, e.g. ``["destination_alias", "arrival_time"]``.
        :return: the decoded JSON reply, with the saved ``order``, or the
            ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when ``columns_configurator_key`` or
            ``order`` is missing.

        .. versionadded:: 1.0.0
        """
        missing = self._missing(kwargs, ["columns_configurator_key", "order"])
        if missing:
            raise ParamValueException(", ".join(missing), "Missing required params")
        return self._call_api(ROUTE_DESTINATIONS_COLUMNS_V5, "put", {}, body=kwargs)

    def get_destination(self, route_destination_id):
        """Get one route destination.

        Sends ``GET /modules/api/v5.0/route-destinations/{route_destination_id}``.

        :param route_destination_id: ID of the destination.
        :return: the decoded JSON reply: the destination, or the
            ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when ``route_destination_id`` is empty.

        .. versionadded:: 1.0.0
        """
        url = f"{ROUTE_DESTINATIONS_V5}/{path_segment(route_destination_id, 'route_destination_id')}"
        return self._call_api(url, "get", {})

    def get_destinations_by_order(self, order_uuid):
        """List the route destinations made from an order.

        Sends ``GET /modules/api/v5.0/route-destinations/order/{order_uuid}``.

        :param order_uuid: UUID of the order.
        :return: the decoded JSON reply: the destinations, or the
            ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when ``order_uuid`` is empty.

        .. versionadded:: 1.0.0
        """
        return self._call_api(f"{ROUTE_DESTINATIONS_BY_ORDER_V5}/{path_segment(order_uuid, 'order_uuid')}", "get", {})

    def get_destination_by_label_code(self, label_code):
        """Find a destination by its label code, with its route and stop context.

        Sends ``GET /modules/api/v5.0/route-destinations/sorting`` with
        ``label_code`` in the query.

        :param label_code: the label code of the destination.
        :return: the decoded JSON reply: the destination, its route, sequence
            number, driver and vehicle, or the ``{"errors": ...}`` dict on an
            API error.
        :raise ParamValueException: when ``label_code`` is empty.

        .. versionadded:: 1.0.0
        """
        params = {"label_code": _required(label_code, "label_code")}
        return self._call_api(ROUTE_DESTINATIONS_SORTING_V5, "get", params)

    def get_destination_sequence(self, coordinates):
        """Get the best visiting sequence of a set of locations.

        Sends ``POST /modules/api/v5.0/route-destinations/sequence`` with
        ``coordinates`` as the JSON body.

        :param coordinates: the locations, a list of ``{"lat": ..., "lng":
            ...}`` dicts.
        :return: the decoded JSON reply, with the sequenced ``items``, or the
            ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when ``coordinates`` is ``None``.

        .. versionadded:: 1.0.0
        """
        body = {"coordinates": _required(coordinates, "coordinates")}
        return self._call_api(ROUTE_DESTINATIONS_SEQUENCE_V5, "post", {}, body=body)
