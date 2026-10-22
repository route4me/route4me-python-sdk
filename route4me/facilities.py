"""The :class:`Facilities` resource (API V5): facilities and facility types."""

from ._url import path_int, path_segment
from .api_endpoints import FACILITIES_V5, FACILITY_TYPES_V5
from .base import Base
from .exceptions import ParamValueException

#: Fields a facility must have when it is created or updated.
FACILITY_REQUIRED_FIELDS = ("facility_alias", "address", "coordinates", "facility_types")


class Facilities(Base):
    """Facilities: depots, warehouses and other sites of an account (API V5).

    Use it as ``route4me.facilities``. Every method sends a request to
    ``/modules/api/v5.0/facilities`` on ``wh.route4me.com``. The methods mirror
    ``FacilityManagerV5`` of the C# SDK.

    Unless stated otherwise, a method returns the decoded JSON reply, or on an
    API error the ``{"errors": ...}`` dict from :meth:`APIException.to_dict
    <route4me.exceptions.APIException.to_dict>` instead of raising.

    .. versionadded:: 1.0.0
    """

    @staticmethod
    def _facility_url(facility_id):
        """Build the URL of one facility, with ``facility_id`` encoded as one path segment.

        :param facility_id: ID of the facility.
        :return: the absolute URL.
        :raise ParamValueException: when ``facility_id`` is empty.
        """
        return f"{FACILITIES_V5}/{path_segment(facility_id, 'facility_id')}"

    def _check_required(self, fields):
        """Check that a facility body has every required field.

        :param fields: the facility fields given.
        :raise ParamValueException: naming the fields that are missing.
        """
        missing = self._missing(fields, FACILITY_REQUIRED_FIELDS)
        if missing:
            raise ParamValueException(", ".join(missing), "Missing required params")

    def get_facilities(self, **kwargs):
        """List the facilities, a page at a time.

        Sends ``GET /modules/api/v5.0/facilities`` with the keywords as query
        parameters. Dict and list values are sent with bracketed keys, e.g.
        ``filters={"status": [1, 2]}`` as ``filters[status][]=1&filters[status][]=2``.

        :param kwargs: optional query parameters: ``search_query``, ``page``,
            ``per_page``, ``filters`` and ``order_by``, a dict of field name to
            ``"asc"`` or ``"desc"``.
        :return: the decoded JSON reply, with the facilities under ``data``,
            or the ``{"errors": ...}`` dict on an API error.

        .. versionadded:: 1.0.0
        """
        return self._call_api(FACILITIES_V5, "get", dict(kwargs))

    def get_facility(self, facility_id):
        """Get one facility.

        Sends ``GET /modules/api/v5.0/facilities/{facility_id}``.

        :param facility_id: ID of the facility.
        :return: the decoded JSON reply: the facility, or the
            ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when ``facility_id`` is empty.

        .. versionadded:: 1.0.0
        """
        return self._call_api(self._facility_url(facility_id), "get", {})

    def create_facility(self, **kwargs):
        """Create a facility.

        Sends ``POST /modules/api/v5.0/facilities`` with the keywords as the
        JSON body.

        :param kwargs: the facility fields. Required: ``facility_alias``;
            ``address``; ``coordinates``, as ``{"lat": ..., "lng": ...}``; and
            ``facility_types``, a list of ``{"facility_type_id": ...,
            "is_default": ...}``. Optional fields include ``status`` (``1``
            active, ``2`` inactive, ``3`` in review), ``custom_data``,
            ``facility_equipment``, ``regions``, ``asset_ids`` and
            ``accountable_person_id``.
        :return: the decoded JSON reply: the new facility, or the
            ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when a required field is missing.

        .. versionadded:: 1.0.0
        """
        self._check_required(kwargs)
        return self._call_api(FACILITIES_V5, "post", {}, body=kwargs)

    def update_facility(self, facility_id, **kwargs):
        """Update a facility.

        Sends ``PUT /modules/api/v5.0/facilities/{facility_id}`` with the
        keywords as the JSON body.

        :param facility_id: ID of the facility.
        :param kwargs: the facility fields, as for :meth:`create_facility`.
            Required: ``facility_alias``, ``address``, ``coordinates`` and
            ``facility_types``.
        :return: the decoded JSON reply: the updated facility, or the
            ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when ``facility_id`` is empty or a
            required field is missing.

        .. versionadded:: 1.0.0
        """
        url = self._facility_url(facility_id)
        self._check_required(kwargs)
        return self._call_api(url, "put", {}, body=kwargs)

    def delete_facility(self, facility_id):
        """Delete a facility.

        Sends ``DELETE /modules/api/v5.0/facilities/{facility_id}``.

        :param facility_id: ID of the facility.
        :return: the decoded JSON reply, or the ``{"errors": ...}`` dict on an
            API error.
        :raise ParamValueException: when ``facility_id`` is empty.

        .. versionadded:: 1.0.0
        """
        return self._call_api(self._facility_url(facility_id), "delete", {})

    def get_facility_types(self):
        """List the facility types.

        Sends ``GET /modules/api/v5.0/facilities/types``.

        :return: the decoded JSON reply, with the types under ``data``, or the
            ``{"errors": ...}`` dict on an API error.

        .. versionadded:: 1.0.0
        """
        return self._call_api(FACILITY_TYPES_V5, "get", {})

    def get_facility_type(self, facility_type_id):
        """Get one facility type.

        Sends ``GET /modules/api/v5.0/facilities/types/{facility_type_id}``.

        :param facility_type_id: ID of the facility type, an integer.
        :return: the decoded JSON reply: the facility type, or the
            ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when ``facility_type_id`` is not a
            non-negative integer.

        .. versionadded:: 1.0.0
        """
        url = f"{FACILITY_TYPES_V5}/{path_int(facility_type_id, 'facility_type_id')}"
        return self._call_api(url, "get", {})
