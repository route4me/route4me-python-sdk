"""The :class:`AddressBarcodes` resource (API V5): barcodes scanned at route stops.

.. versionadded:: 1.0.0
"""

from .api_endpoints import ADDRESS_BARCODES_V5
from .base import Base
from .exceptions import ParamValueException


class AddressBarcodes(Base):
    """Address barcodes: the barcodes scanned at the stops of a route (API V5).

    Use it as ``route4me.address_barcodes``. It mirrors the C# SDK's
    ``AddressBarcodeManagerV5``. Every method sends a request to
    ``/modules/api/v5.0/address-barcodes`` on ``wh.route4me.com``; the client
    sends the API key as a bearer token.

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

    def _check_required(self, params, required):
        """Raise when a required field is missing.

        :param params: the fields given.
        :param required: the names that must be present.
        :raise ParamValueException: naming every missing field.
        """
        missing = self._missing(params, required)
        if missing:
            raise ParamValueException(", ".join(missing), "Missing required params")

    def get_address_barcodes(self, **kwargs):
        """List the barcodes scanned on a route, one page at a time.

        Sends ``GET /modules/api/v5.0/address-barcodes``.

        :param kwargs: query parameters. Required: ``route_id``. Optional:
            ``route_destination_id``, to keep one stop; ``limit``; and
            ``cursor``, the ``next_page_cursor`` of the previous page.
        :return: the decoded JSON reply: ``status``, ``data`` (the barcodes)
            and ``next_page_cursor``, or the ``{"errors": ...}`` dict on an API
            error.
        :raise ParamValueException: when ``route_id`` is missing.

        .. versionadded:: 1.0.0
        """
        self._check_required(kwargs, ["route_id"])
        return self._call_api(ADDRESS_BARCODES_V5, "get", dict(kwargs))

    def save_address_barcodes(self, **kwargs):
        """Save barcodes scanned at a route stop.

        Sends ``POST /modules/api/v5.0/address-barcodes`` with the keywords as
        the JSON body.

        :param kwargs: the body. Required: ``route_id``,
            ``route_destination_id`` (the stop) and ``barcodes``, a list of
            scans. Each scan has ``barcode`` and ``scan_type`` (both required),
            and optionally ``lat``, ``lng``, ``timestamp_date``,
            ``timestamp_utc`` (Unix seconds) and ``scanned_at``
            (``"YYYY-MM-DD HH:MM:SS"``).
        :return: the decoded JSON reply, e.g. ``{"status": true}``, or the
            ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when a required field is missing.

        .. versionadded:: 1.0.0
        """
        self._check_required(kwargs, ["route_id", "route_destination_id", "barcodes"])
        return self._call_api(ADDRESS_BARCODES_V5, "post", {}, body=kwargs)
