import warnings

from ._api_method import make_request
from .api_endpoints import (
    ADDRESS_HOST,
    DUPLICATE_ROUTE,
    EXPORTER,
    EXPORTER_V5,
    GET_ACTIVITIES_HOST,
    MERGE_ROUTES_HOST,
    RESEQUENCE_ROUTE,
    ROUTE_HOST,
    SHARE_ROUTE_HOST,
)
from .base import Base
from .exceptions import APIException, ParamValueException


class Route(Base):
    """
    A Route is a multi-sequence of addresses that need to be
    visited by a single vehicle and a single driver in a fixed time period.
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
        if self.validate_params(**kwargs):
            self.params.update(kwargs)
        return make_request(self, ROUTE_HOST, "get", self.params, required=self.requirements)

    def get_route_tracking(self, **kwargs):
        if self.validate_params(**kwargs):
            self.params.update(kwargs)
        self.params.update({"device_tracking_history": 1})
        return make_request(self, ROUTE_HOST, "get", self.params, required=self.requirements)

    def get_routes(self, **kwargs):
        kwargs.update({"api_key": self.params["api_key"]})
        return make_request(self, ROUTE_HOST, "get", kwargs, required=["limit", "offset"])

    def get_activities(self, **kwargs):
        kwargs.update({"api_key": self.params["api_key"]})
        return make_request(self, GET_ACTIVITIES_HOST, "get", kwargs, required=["route_id", "limit", "offset"])

    def duplicate_route(self, **kwargs):
        kwargs.update({"api_key": self.params["api_key"]})
        return make_request(self, DUPLICATE_ROUTE, "get", kwargs, required=["route_id"])

    def delete_routes(self, **kwargs):
        """
        Delete routes using DELETE request
        :return: API response
        :raise: ParamValueException if required params are not present.
        """
        kwargs.update({"api_key": self.params["api_key"]})
        if self.check_required_params(kwargs, ["route_id"]):
            kwargs["route_id"] = ",".join(kwargs["route_id"])
            try:
                self.response = self.api._make_request(ROUTE_HOST, kwargs, self.api._request_delete)
                return self.response.json()
            except APIException as e:
                return e.to_dict()
        else:
            raise ParamValueException("params", "Params are not complete")

    def delete_route(self, **kwargs):
        """
        Delete given route
        :return: API response
        :raises: ParamValueException if required params are not present.
        AttributeError if there is an error deleting a route
        """
        kwargs.update({"api_key": self.params["api_key"]})
        if self.check_required_params(kwargs, ["route_id"]):
            try:
                self.response = self.api._make_request(ROUTE_HOST, kwargs, self.api._request_delete)
                response = self.response.json()
                try:
                    response = response.get("deleted")
                    return response
                except AttributeError:
                    return response.errors
            except APIException as e:
                return e.to_dict()
        else:
            raise ParamValueException("params", "Params are not complete")

    def insert_address_into_route(self, addresses, route_id):
        params = {"route_id": route_id}
        return self._update_route(params, addresses)

    def move_addresses_from_route(self, addresses, route_id):
        params = {"route_id": route_id}
        return self._update_route(params, addresses)

    def update_route_parameters(self, data, route_id):
        params = {"route_id": route_id}
        return self._update_route(params, data)

    def update_route(self, data, route_id):
        params = {"route_id": route_id}
        return self._update_route(params, data)

    def insert_address_into_route_optimal_position(self, **kwargs):
        """
        Insert an address into a route in an optimal position using PUT
        """
        if self.check_required_params(kwargs, ["addresses", "route_id", "optimal_position"]):
            params = {"api_key": self.params["api_key"], "route_id": kwargs.pop("route_id")}
            try:
                self.response = self.api._make_request(ROUTE_HOST, params, self.api._request_put, json=kwargs)
                return self.response.json()
            except APIException as e:
                return e.to_dict()
        else:
            raise ParamValueException("params", "Params are not complete")

    def get_route_path_points(self, **kwargs):
        kwargs.update({"api_key": self.params["api_key"]})
        return make_request(self, ROUTE_HOST, "get", kwargs, required=["route_path_output", "route_id"])

    def get_route_directions(self, **kwargs):
        kwargs.update({"api_key": self.params["api_key"]})
        return make_request(self, ROUTE_HOST, "get", kwargs, required=["directions", "route_id"])

    def share_route(self, **kwargs):
        """
        Share a route using POST
        """
        if self.check_required_params(kwargs, ["recipient_email", "route_id", "response_format"]):
            params = {
                "api_key": self.params["api_key"],
                "route_id": kwargs.pop("route_id"),
                "response_format": kwargs.pop("response_format"),
            }
            try:
                self.response = self.api._make_request(SHARE_ROUTE_HOST, params, self.api._request_post, json=kwargs)
                return self.response.json()
            except APIException as e:
                return e.to_dict()
        else:
            raise ParamValueException("params", "Params are not complete")

    def resequence_route(self, **kwargs):
        """
        Resequence a route using PUT
        """
        if self.check_required_params(kwargs, ["addresses", "route_id", "route_destination_id"]):
            params = {
                "api_key": self.params["api_key"],
                "route_id": kwargs.pop("route_id"),
                "route_destination_id": kwargs.pop("route_destination_id"),
            }
            try:
                self.response = self.api._make_request(ROUTE_HOST, params, self.api._request_put, json=kwargs)
                return self.response.json()
            except APIException as e:
                return e.to_dict()
        else:
            raise ParamValueException("params", "Params are not complete")

    def resequence_multiple_stops(self, route_id, addresses_data):
        if self.check_required_params(addresses_data, ["addresses"]):
            params = {
                "api_key": self.params["api_key"],
                "route_id": route_id,
            }
            return make_request(self, ROUTE_HOST, "put", params, body=addresses_data)
        else:
            raise ParamValueException("params", "Params are not complete")

    def merge_routes(self, **kwargs):
        if not self.check_required_params(kwargs, ["route_ids"]):
            raise ParamValueException("params", "Params are not complete")
        return make_request(self, MERGE_ROUTES_HOST, "post", self.params, body=kwargs, body_key="data")

    def resequence_route_all(self, **kwargs):
        kwargs.update({"api_key": self.params["api_key"]})
        return make_request(
            self, RESEQUENCE_ROUTE, "get", kwargs, required=["disable_optimization", "route_id", "optimize"]
        )

    def update_route_destination_custom_data(self, **kwargs):
        """
        Update route destination custom data using PUT
        """
        if self.check_required_params(kwargs, ["route_id", "route_destination_id"]):
            params = {
                "api_key": self.params["api_key"],
                "route_id": kwargs.pop("route_id"),
                "route_destination_id": kwargs.pop("route_destination_id"),
            }
            return make_request(self, ADDRESS_HOST, "put", params, body=kwargs)
        else:
            raise ParamValueException("params", "Params are not complete")

    def export_route(self, route_id, output_format="csv"):
        warnings.warn("export_route is deprecated. Please use export_route_v5", DeprecationWarning, stacklevel=2)
        data = {"route_id": route_id, "strExportFormat": output_format}
        self.response = self.api._make_request(EXPORTER, {}, self.api._request_post, data=data)
        return self.response.content

    def _update_route(self, params, data):
        params.update({"api_key": self.api.key})
        try:
            response = self.api._make_request(ROUTE_HOST, params, self.api._request_put, data=data)
            return response.json()
        except APIException as e:
            return e.to_dict()

    def export_route_v5(self, route_id, output_format="csv", all_custom_fields=True, columns=None):
        params = {
            "api_key": self.params["api_key"],
        }
        data = {"all_custom_fields": all_custom_fields, "format": output_format}
        if columns is not None:
            data["columns"] = columns
        try:
            self.response = self.api._make_request(
                EXPORTER_V5.format(route_id=route_id), params, self.api._request_post, data=data
            )
            return self.response.content
        except APIException as e:
            return e.to_dict()
