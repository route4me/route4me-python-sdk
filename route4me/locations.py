"""The :class:`Locations` resource (API V5): address book locations and location types."""

from ._url import path_segment
from .api_endpoints import (
    LOCATION_TYPES_V5,
    LOCATIONS_CLUSTERING_V5,
    LOCATIONS_EXPORT_COLUMNS_V5,
    LOCATIONS_EXPORT_V5,
    LOCATIONS_HEATMAP_V5,
    LOCATIONS_LIST_COMBINED_V5,
    LOCATIONS_LIST_V5,
    LOCATIONS_TERRITORIES_V5,
)
from .base import Base
from .exceptions import ParamValueException

#: Fields a location type must have when it is created or updated.
LOCATION_TYPE_REQUIRED_FIELDS = ("name", "is_parent_type", "is_child_type")


class Locations(Base):
    """Locations: the places of the address book, and their types (API V5).

    Use it as ``route4me.locations``. Every method sends a request to
    ``/modules/api/v5.0/address-book/locations`` on ``wh.route4me.com``. The
    methods mirror ``LocationManagerV5`` of the C# SDK.

    The location queries (:meth:`get_locations_list` and the methods after it)
    take the same JSON body: ``filters``, a dict such as
    ``{"search_query": "Main St"}``; ``order_by``, a list of
    ``[field, direction]`` pairs; ``page``; ``per_page``; ``group_by``;
    ``fields``; and ``selected_fields``, the fields to return. All of them are
    optional.

    Unless stated otherwise, a method returns the decoded JSON reply, or on an
    API error the ``{"errors": ...}`` dict from :meth:`APIException.to_dict
    <route4me.exceptions.APIException.to_dict>` instead of raising.

    .. versionadded:: 1.0.0
    """

    @staticmethod
    def _location_type_url(location_type_id):
        """Build the URL of one location type, with its ID encoded as one path segment.

        :param location_type_id: ID of the location type.
        :return: the absolute URL.
        :raise ParamValueException: when ``location_type_id`` is empty.
        """
        return f"{LOCATION_TYPES_V5}/{path_segment(location_type_id, 'location_type_id')}"

    def _check_required(self, fields):
        """Check that a location type body has every required field.

        :param fields: the location type fields given.
        :raise ParamValueException: naming the fields that are missing.
        """
        missing = self._missing(fields, LOCATION_TYPE_REQUIRED_FIELDS)
        if missing:
            raise ParamValueException(", ".join(missing), "Missing required params")

    def get_locations_list(self, **kwargs):
        """List the locations, a page at a time.

        Sends ``POST /modules/api/v5.0/address-book/locations/list`` with the
        keywords as the JSON body.

        :param kwargs: the query fields described in the class docstring.
        :return: the decoded JSON reply, with the locations under ``items``,
            or the ``{"errors": ...}`` dict on an API error.

        .. versionadded:: 1.0.0
        """
        return self._call_api(LOCATIONS_LIST_V5, "post", {}, body=kwargs)

    def get_locations_combined(self, **kwargs):
        """List the locations together with their column configuration.

        Sends ``POST /modules/api/v5.0/address-book/locations/list/combined``
        with the keywords as the JSON body.

        :param kwargs: the query fields described in the class docstring.
        :return: the decoded JSON reply, with the locations under ``data`` and
            the columns under ``config``, or the ``{"errors": ...}`` dict on an
            API error.

        .. versionadded:: 1.0.0
        """
        return self._call_api(LOCATIONS_LIST_COMBINED_V5, "post", {}, body=kwargs)

    def get_locations_clustering(self, **kwargs):
        """Group the locations into map clusters.

        Sends ``POST /modules/api/v5.0/address-book/locations/clustering`` with
        the keywords as the JSON body.

        :param kwargs: the query fields described in the class docstring, plus
            ``clustering``, e.g. ``{"zoom": 10}``, and ``with_clusters``.
        :return: the decoded JSON reply: the clusters, or the
            ``{"errors": ...}`` dict on an API error.

        .. versionadded:: 1.0.0
        """
        return self._call_api(LOCATIONS_CLUSTERING_V5, "post", {}, body=kwargs)

    def get_locations_heatmap(self, **kwargs):
        """Get a heat map of the locations.

        Sends ``POST /modules/api/v5.0/address-book/locations/heatmap`` with
        the keywords as the JSON body.

        :param kwargs: the query fields described in the class docstring, plus
            ``zoom``.
        :return: the decoded JSON reply: the heat map points, or the
            ``{"errors": ...}`` dict on an API error.

        .. versionadded:: 1.0.0
        """
        return self._call_api(LOCATIONS_HEATMAP_V5, "post", {}, body=kwargs)

    def get_locations_territories(self, **kwargs):
        """List the territories with the number of locations in each.

        Sends ``POST /modules/api/v5.0/address-book/locations/territories``
        with the keywords as the JSON body.

        :param kwargs: the query fields described in the class docstring, plus
            ``territories_page``, ``territories_per_page``,
            ``territories_search_query`` and ``territories_order_by``.
        :return: the decoded JSON reply: the territories, or the
            ``{"errors": ...}`` dict on an API error.

        .. versionadded:: 1.0.0
        """
        return self._call_api(LOCATIONS_TERRITORIES_V5, "post", {}, body=kwargs)

    def get_locations_export_columns(self, **kwargs):
        """List the columns a location export can have.

        Sends ``POST /modules/api/v5.0/address-book/locations/export/columns``
        with the keywords as the JSON body.

        :param kwargs: the query fields described in the class docstring, plus
            ``address_ids`` and ``excluded_ids``.
        :return: the decoded JSON reply: the columns, or the
            ``{"errors": ...}`` dict on an API error.

        .. versionadded:: 1.0.0
        """
        return self._call_api(LOCATIONS_EXPORT_COLUMNS_V5, "post", {}, body=kwargs)

    def export_locations(self, **kwargs):
        """Start an export of the locations.

        Sends ``POST /modules/api/v5.0/address-book/locations/export`` with the
        keywords as the JSON body. The API accepts the export with
        ``202 Accepted`` and prepares the file in the background.

        :param kwargs: the query fields described in the class docstring, plus
            ``columns``, from :meth:`get_locations_export_columns`;
            ``address_ids``; ``excluded_ids``; ``filename``; ``format``; and
            ``tz``, the time zone.
        :return: the decoded JSON reply, the raw body (``bytes``, empty for a
            reply without content) when it is not JSON, or the
            ``{"errors": ...}`` dict on an API error.

        .. versionadded:: 1.0.0
        """
        return self._request_decoded(LOCATIONS_EXPORT_V5, {}, "post", json=kwargs)

    def get_location_types(self, **kwargs):
        """List the location types.

        Sends ``GET /modules/api/v5.0/address-book/locations/types`` with the
        keywords as query parameters. A dict value is sent with bracketed keys,
        e.g. ``filters={"is_parent_type": 1}`` as ``filters[is_parent_type]=1``.

        :param kwargs: optional query parameters: ``page``, ``per_page`` and
            ``filters``, with ``is_parent_type``, ``is_child_type``,
            ``only_custom_types`` and ``search_query``.
        :return: the decoded JSON reply, with the location types under
            ``data``, or the ``{"errors": ...}`` dict on an API error.

        .. versionadded:: 1.0.0
        """
        return self._call_api(LOCATION_TYPES_V5, "get", dict(kwargs))

    def get_location_type_by_id(self, location_type_id):
        """Get one location type.

        Sends ``GET /modules/api/v5.0/address-book/locations/types/{location_type_id}``.

        :param location_type_id: ID of the location type.
        :return: the decoded JSON reply: the location type, or the
            ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when ``location_type_id`` is empty.

        .. versionadded:: 1.0.0
        """
        return self._call_api(self._location_type_url(location_type_id), "get", {})

    def create_location_type(self, **kwargs):
        """Create a location type.

        Sends ``POST /modules/api/v5.0/address-book/locations/types`` with the
        keywords as the JSON body.

        :param kwargs: the location type fields. Required: ``name``;
            ``is_parent_type``, whether locations of this type can contain
            other locations; and ``is_child_type``, whether they can be inside
            another location. Optional: ``description``.
        :return: the decoded JSON reply: the new location type, or the
            ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when a required field is missing.

        .. versionadded:: 1.0.0
        """
        self._check_required(kwargs)
        return self._call_api(LOCATION_TYPES_V5, "post", {}, body=kwargs)

    def update_location_type(self, location_type_id, **kwargs):
        """Update a location type.

        Sends ``PUT /modules/api/v5.0/address-book/locations/types/{location_type_id}``
        with the keywords as the JSON body.

        :param location_type_id: ID of the location type.
        :param kwargs: the location type fields, as for
            :meth:`create_location_type`. Required: ``name``,
            ``is_parent_type`` and ``is_child_type``.
        :return: the decoded JSON reply: the updated location type, or the
            ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when ``location_type_id`` is empty or a
            required field is missing.

        .. versionadded:: 1.0.0
        """
        url = self._location_type_url(location_type_id)
        self._check_required(kwargs)
        return self._call_api(url, "put", {}, body=kwargs)

    def delete_location_type(self, location_type_id):
        """Delete a location type.

        Sends ``DELETE /modules/api/v5.0/address-book/locations/types/{location_type_id}``.

        :param location_type_id: ID of the location type.
        :return: the decoded JSON reply, e.g. ``{"status": True}``, or the
            ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when ``location_type_id`` is empty.

        .. versionadded:: 1.0.0
        """
        return self._call_api(self._location_type_url(location_type_id), "delete", {})
