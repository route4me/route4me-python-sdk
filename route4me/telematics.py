"""The :class:`Telematics` resource: telematics vendors and the connections to them."""

import warnings

from .api_endpoints import (
    TELEMATICS_CONNECTIONS_V4,
    TELEMATICS_REGISTER_V4,
    TELEMATICS_VENDORS_ALL_V5,
    TELEMATICS_VENDORS_INFO_V4,
    TELEMATICS_VENDORS_V4,
    TELEMATICS_VENDORS_V5,
)
from .base import Base
from .exceptions import APIException, ParamValueException


def _warn_retired(method, replacement):
    """Warn that a vendor method calls the retired ``telematics.route4me.com`` host.

    :param method: name of the deprecated method.
    :param replacement: name of the method to use instead.
    """
    warnings.warn(
        f"Telematics.{method} is deprecated: telematics.route4me.com is retired. Use Telematics.{replacement}.",
        DeprecationWarning,
        stacklevel=3,
    )


class Telematics(Base):
    """Telematics: the vendors Route4Me integrates with, and connections to them.

    Use it as ``route4me.telematics``. The connection methods take the
    member's telematics ``api_token``, which :meth:`register_member` returns.

    Unless stated otherwise, a method returns the decoded JSON reply, or on an
    API error the ``{"errors": ...}`` dict from :meth:`APIException.to_dict
    <route4me.exceptions.APIException.to_dict>` instead of raising.
    """

    def __init__(self, api):
        """Create the resource.

        :param api: the :class:`~route4me.api.Route4Me` client.
        """
        Base.__init__(self, api)

    @staticmethod
    def pp_response(response, file=None):
        """Pretty-print a telematics response.

        A display helper, not library logging -- printing is the whole point of
        a ``pp_`` function, and twelve scripts under ``examples/telematics/``
        depend on it writing to stdout. Routing it through ``logging`` would
        silently produce no output for all of them, since examples do not
        configure a handler.

        Prints one ``key : value`` line per item, then a blank line. Anything
        other than a dict prints nothing.

        :param response: the decoded reply to print.
        :param file: destination stream; defaults to stdout. Pass an
            ``io.StringIO`` to capture the output instead.
        """
        if isinstance(response, dict):
            for k, v in response.items():
                print(f"{k} : {v}", file=file)
            print("", file=file)

    @staticmethod
    def pp_vendor_comparison(vendor, file=None):
        """Pretty-print one vendor's feature list as a tab-separated row.

        See :meth:`pp_response` on why this prints rather than logs.

        Prints the vendor's ``id``, ``name`` and feature names. Anything other
        than a dict prints nothing.

        :param vendor: one vendor, as decoded from a reply.
        :param file: destination stream; defaults to stdout.

        .. deprecated:: 1.0.0
           Only the retired :meth:`compare_vendors` reply lists ``features``;
           API V5 vendors have none. Print the fields of the
           :meth:`get_vendor_v5` reply instead.
        """
        warnings.warn(
            "Telematics.pp_vendor_comparison is deprecated: it prints the features of the retired "
            "compare_vendors reply, and API V5 vendors have none.",
            DeprecationWarning,
            stacklevel=2,
        )
        if isinstance(vendor, dict):
            features = [x["name"] for x in vendor.get("features", [])]
            print(f"{vendor.get('id')}\t{vendor.get('name')}\t{', '.join(features)}", file=file)

    def get_vendors_v5(self, **kwargs):
        """List the telematics vendors with API V5.

        Sends ``GET /modules/api/v5.0/telematics/vendors/all``.

        :param kwargs: optional filters, sent as query parameters: ``search``,
            ``country``, ``feature``, ``features``, ``size``, ``is_integrated``,
            ``display_hidden``, ``page`` and ``per_page``.
        :return: the decoded JSON reply, with the vendors under ``data``, or
            the ``{"errors": ...}`` dict on an API error.

        .. versionadded:: 1.0.0
           Replaces :meth:`get_vendors` and :meth:`search_vendor`.
        """
        return self._call_api(TELEMATICS_VENDORS_ALL_V5, "get", dict(kwargs, api_key=self.api.key))

    def get_vendor_v5(self, vendor_id):
        """Get one telematics vendor with API V5.

        Sends ``GET /modules/api/v5.0/telematics/vendors`` with ``vendor_id``.

        :param vendor_id: ID of the vendor.
        :return: the decoded JSON reply: the vendor, or the ``{"errors": ...}``
            dict on an API error.

        .. versionadded:: 1.0.0
           Replaces :meth:`get_vendor`.
        """
        return self._call_api(TELEMATICS_VENDORS_V5, "get", {"api_key": self.api.key, "vendor_id": vendor_id})

    def get_vendors(self):
        """List the telematics vendors.

        Sends ``GET /api/vendors.php`` to ``telematics.route4me.com``.

        :return: the decoded JSON reply: the vendors, or the
            ``{"errors": ...}`` dict on an API error.

        .. deprecated:: 1.0.0
           ``telematics.route4me.com`` is retired and redirects to the website,
           so this call cannot succeed. Use :meth:`get_vendors_v5`.
        """
        _warn_retired("get_vendors", "get_vendors_v5")
        return self._call_api(TELEMATICS_VENDORS_V4, "get", {"api_key": self.api.key})

    def get_vendor(self, vendor_id):
        """Get one telematics vendor.

        Sends ``GET /api/vendors.php`` to ``telematics.route4me.com`` with
        ``vendor_id``.

        :param vendor_id: ID of the vendor.
        :return: the decoded JSON reply: the vendor, or the ``{"errors": ...}``
            dict on an API error.

        .. deprecated:: 1.0.0
           ``telematics.route4me.com`` is retired. Use :meth:`get_vendor_v5`.
        """
        _warn_retired("get_vendor", "get_vendor_v5")
        params = {"api_key": self.api.key, "vendor_id": vendor_id}
        return self._call_api(TELEMATICS_VENDORS_V4, "get", params)

    def search_vendor(self, **kwargs):
        """Search the telematics vendors.

        Sends ``GET /api/vendors.php`` to ``telematics.route4me.com``.

        :param kwargs: search filters, sent as query parameters as is.
        :return: the decoded JSON reply: the matching vendors, or the
            ``{"errors": ...}`` dict on an API error.

        .. deprecated:: 1.0.0
           ``telematics.route4me.com`` is retired. Use :meth:`get_vendors_v5`,
           which takes the same filters.
        """
        _warn_retired("search_vendor", "get_vendors_v5")
        return self._call_api(TELEMATICS_VENDORS_V4, "get", dict(kwargs, api_key=self.api.key))

    def compare_vendors(self, vendors_id):
        """Compare several telematics vendors.

        Sends ``GET /api/vendors.php`` to ``telematics.route4me.com`` with
        ``vendors``.

        :param vendors_id: the vendor IDs, comma-separated, e.g. ``"55,56"``.
        :return: the decoded JSON reply: the vendors, or the
            ``{"errors": ...}`` dict on an API error.

        .. deprecated:: 1.0.0
           ``telematics.route4me.com`` is retired and API V5 has no comparison
           endpoint. Fetch each vendor with :meth:`get_vendor_v5`.
        """
        _warn_retired("compare_vendors", "get_vendor_v5")
        params = {"api_key": self.api.key, "vendors": vendors_id}
        return self._call_api(TELEMATICS_VENDORS_V4, "get", params)

    def register_member(self, member_id):
        """Register a member with the telematics service.

        Sends ``GET /api.v4/telematics/register.php`` with ``member_id``.

        :param member_id: ID of the member.
        :return: the decoded JSON reply, with the member's ``api_token``, or
            the ``{"errors": ...}`` dict on an API error.
        """
        params = {"api_key": self.api.key, "member_id": member_id}
        return self._call_api(TELEMATICS_REGISTER_V4, "get", params)

    def get_connections(self, api_token, **kwargs):
        """List a member's telematics connections.

        Sends ``GET /api.v4/telematics/connections.php``.

        :param api_token: the member's telematics API token.
        :param kwargs: further query parameters, sent as is.
        :return: the decoded JSON reply: the connections, or the
            ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: if the query has no ``api_token``. The
            argument is always added, so this is not raised in practice.
        """
        kwargs.update({"api_token": api_token})

        if self.check_required_params(kwargs, ["api_token"]):
            try:
                self.response = self._request(TELEMATICS_CONNECTIONS_V4, kwargs, "get")
                return self.response.json()
            except APIException as e:
                return e.to_dict()
        else:
            raise ParamValueException("params", "Missing API Token")

    def get_vendors_info(self, api_token, **kwargs):
        """Get information on the vendors a member is connected to.

        Sends ``GET /api.v4/telematics/vendors.php``.

        :param api_token: the member's telematics API token.
        :param kwargs: further query parameters, sent as is.
        :return: the decoded JSON reply, or the ``{"errors": ...}`` dict on an
            API error.
        :raise ParamValueException: if the query has no ``api_token``. The
            argument is always added, so this is not raised in practice.
        """
        kwargs.update({"api_token": api_token})

        if self.check_required_params(kwargs, ["api_token"]):
            try:
                self.response = self._request(TELEMATICS_VENDORS_INFO_V4, kwargs, "get")
                return self.response.json()
            except APIException as e:
                return e.to_dict()
        else:
            raise ParamValueException("params", "Missing API Token")

    def register_connection(self, api_token, **kwargs):
        """Create a connection to a telematics vendor.

        Sends ``POST /api.v4/telematics/connections.php`` with the keywords
        and ``validate_remote_credentials="true"`` as the JSON body.

        :param api_token: the member's telematics API token.
        :param kwargs: the connection fields, e.g. the vendor credentials.
            Required: ``vendor_id``.
        :return: the decoded JSON reply: the new connection, or the
            ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when ``vendor_id`` is missing.
        """
        params = {"api_token": api_token}
        kwargs.update({"validate_remote_credentials": "true"})
        if self.check_required_params(kwargs, ["vendor_id"]):
            try:
                self.response = self._request(TELEMATICS_CONNECTIONS_V4, params, "post", json=kwargs)
                return self.response.json()
            except APIException as e:
                return e.to_dict()
        else:
            raise ParamValueException("params", "Missing Vendor ID")

    def get_connection(self, api_token, connection_token):
        """Get one telematics connection.

        Sends ``GET /api.v4/telematics/connections.php``.

        :param api_token: the member's telematics API token.
        :param connection_token: token of the connection.
        :return: the decoded JSON reply: the connection, or the
            ``{"errors": ...}`` dict on an API error.
        """
        params = {"api_token": api_token, "connection_token": connection_token}
        try:
            self.response = self._request(TELEMATICS_CONNECTIONS_V4, params, "get")
            return self.response.json()
        except APIException as e:
            return e.to_dict()

    def delete_connection(self, api_token, connection_token):
        """Delete a telematics connection.

        Sends ``DELETE /api.v4/telematics/connections.php``.

        :param api_token: the member's telematics API token.
        :param connection_token: token of the connection.
        :return: the decoded JSON reply, or the ``{"errors": ...}`` dict on an
            API error.
        """
        params = {"api_token": api_token, "connection_token": connection_token}
        try:
            self.response = self._request(TELEMATICS_CONNECTIONS_V4, params, "delete")
            return self.response.json()
        except APIException as e:
            return e.to_dict()

    def update_connection(self, api_token, connection_token, **kwargs):
        """Update a telematics connection.

        Sends ``PUT /api.v4/telematics/connections.php`` with the keywords and
        ``validate_remote_credentials="true"`` as the JSON body.

        :param api_token: the member's telematics API token.
        :param connection_token: token of the connection.
        :param kwargs: the fields to change. Required: ``vendor_id``.
        :return: the decoded JSON reply: the updated connection, or the
            ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when ``vendor_id`` is missing.
        """
        params = {"api_token": api_token, "connection_token": connection_token}
        kwargs.update({"validate_remote_credentials": "true"})
        if self.check_required_params(kwargs, ["vendor_id"]):
            try:
                self.response = self._request(TELEMATICS_CONNECTIONS_V4, params, "put", json=kwargs)
                return self.response.json()
            except APIException as e:
                return e.to_dict()
        else:
            raise ParamValueException("params", "Missing Vendor ID")
