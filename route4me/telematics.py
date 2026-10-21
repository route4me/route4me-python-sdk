from .api_endpoints import (
    TELEMATICS_CONNECTIONS_V4,
    TELEMATICS_REGISTER_V4,
    TELEMATICS_VENDORS_INFO_V4,
    TELEMATICS_VENDORS_V4,
)
from .base import Base
from .exceptions import APIException, ParamValueException


class Telematics(Base):
    """
    Telematics Management
    """

    def __init__(self, api):
        """
        Telematics Instance
        :param api:
        :return:
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

        :param file: destination stream; defaults to stdout.
        """
        if isinstance(vendor, dict):
            features = [x["name"] for x in vendor.get("features", [])]
            print(f"{vendor.get('id')}\t{vendor.get('name')}\t{', '.join(features)}", file=file)

    def get_vendors(self):
        if self.check_required_params(
            self.params,
            [
                "api_key",
            ],
        ):
            try:
                self.response = self._request(TELEMATICS_VENDORS_V4, self.params, "get")
                return self.response.json()
            except APIException as e:
                return e.to_dict()
        else:
            raise ParamValueException("params", "Missing API KEY")

    def get_vendor(self, vendor_id):

        self.params.update({"vendor_id": vendor_id})

        if self.check_required_params(self.params, ["api_key"]):
            try:
                self.response = self._request(TELEMATICS_VENDORS_V4, self.params, "get")
                return self.response.json()
            except APIException as e:
                return e.to_dict()
        else:
            raise ParamValueException("params", "Missing API KEY")

    def search_vendor(self, **kwargs):

        kwargs.update(
            {
                "api_key": self.params["api_key"],
            }
        )

        if self.check_required_params(kwargs, ["api_key"]):
            try:
                self.response = self._request(TELEMATICS_VENDORS_V4, kwargs, "get")
                return self.response.json()
            except APIException as e:
                return e.to_dict()
        else:
            raise ParamValueException("params", "Missing API KEY")

    def compare_vendors(self, vendors_id):

        self.params.update({"vendors": vendors_id})

        if self.check_required_params(self.params, ["api_key"]):
            try:
                self.response = self._request(TELEMATICS_VENDORS_V4, self.params, "get")
                return self.response.json()
            except APIException as e:
                return e.to_dict()
        else:
            raise ParamValueException("params", "Missing API KEY")

    def register_member(self, member_id):
        self.params.update({"member_id": member_id})

        if self.check_required_params(self.params, ["api_key"]):
            try:
                self.response = self._request(TELEMATICS_REGISTER_V4, self.params, "get")
                return self.response.json()
            except APIException as e:
                return e.to_dict()
        else:
            raise ParamValueException("params", "Missing API KEY")

    def get_connections(self, api_token, **kwargs):
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
        params = {"api_token": api_token, "connection_token": connection_token}
        try:
            self.response = self._request(TELEMATICS_CONNECTIONS_V4, params, "get")
            return self.response.json()
        except APIException as e:
            return e.to_dict()

    def delete_connection(self, api_token, connection_token):
        params = {"api_token": api_token, "connection_token": connection_token}
        try:
            self.response = self._request(TELEMATICS_CONNECTIONS_V4, params, "delete")
            return self.response.json()
        except APIException as e:
            return e.to_dict()

    def update_connection(self, api_token, connection_token, **kwargs):
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
