# -*- coding: utf-8 -*-

from ._api_method import make_request
from .api_endpoints import ADDRESS_HOST, API_HOST
from .base import Base
from .exceptions import ParamValueException, APIException
from .slowdowns import Slowdowns
from .utils import is_valid_datetime


class Optimization(Base):
    """
    An Optimization Problem is a collection of addresses that need to be
    visited. This is distinct from a Route, which is a sequence of
    addresses that need to be visited by a single vehicle and a single
    driver in a fixed time period. Solving an Optimization Problem
    results in a number of routes.
    """

    def __init__(self, api):
        Base.__init__(self, api)

    def get_optimizations(self, **kwargs):
        kwargs.update({"api_key": self.params["api_key"]})
        return make_request(self, API_HOST, 'get', kwargs,
                            required=['limit', 'offset'])

    def get_optimization(self, **kwargs):
        kwargs.update({"api_key": self.params["api_key"]})
        return make_request(self, API_HOST, 'get', kwargs,
                            required=['optimization_problem_id'])

    def update_optimization(self, **kwargs):
        """
        Update optimization using PUT request
        :return: API response
        :raise: ParamValueException if required params are not present.
        """
        kwargs.update({"api_key": self.params["api_key"]})
        if self.check_required_params(
            kwargs, ["optimization_problem_id", "addresses", "reoptimize"]
        ):
            try:
                response = self.api._make_request(
                    API_HOST, self.params, self.api._request_put, data=kwargs
                )
                return response.json()
            except APIException as e:
                return e.to_dict()
        else:
            raise ParamValueException("params", "Params are not complete")

    def delete_optimization(self, **kwargs):
        self.json_data = kwargs
        if not self.check_required_params(kwargs, ['optimization_problem_ids']):
            raise ParamValueException("params", "Params are not complete")
        return make_request(self, API_HOST, 'delete', self.params, body=kwargs)

    def delete_address_from_optimization(self, **kwargs):
        kwargs.update({"api_key": self.params["api_key"]})
        return make_request(self, ADDRESS_HOST, 'delete', kwargs,
                            required=['optimization_problem_id', 'route_destination_id'])

    def set_slowdowns(self, service_time, travel_time):
        slowdowns = Slowdowns(service_time, travel_time)
        self._copy_data({"slowdowns": slowdowns.to_dict()})

    def set_order_aggregation_groups(
        self,
        scheduled_for_range,
        aggregations_id,
        order_status,
        aggregation_profile_overrides,
        split=True,
    ):
        order_aggregation_groups = {
            "split": split,
            "aggregations_id": aggregations_id,
            "filters": {
                "scheduled_for_range": scheduled_for_range,
                "order_status": order_status,
            },
            "aggregation_profile_overrides": aggregation_profile_overrides,
        }
        self.data.update({"order_aggregation_groups": order_aggregation_groups})

    def route_start_date_local(self, route_start_date_local):
        if not is_valid_datetime(route_start_date_local, "%Y-%m-%d"):
            raise ParamValueException(
                "params",
                "Route Start Date Local is invalid, must be YYYY-MM-DD date format",
            )
        self._copy_data({"route_start_date_local": route_start_date_local})
