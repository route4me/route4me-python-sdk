# -*- coding: utf-8 -*-
from .base import Base
from .exceptions import ParamValueException, APIException
from .utils import is_valid_datetime

from .api_endpoints import ORDERS_GROUP_V5, ASSIGN_PROFILES_V5


class OrdersGroup(Base):

    def __init__(self, api):
        """
        Order Groups Instance
        :param api:
        :return:
        """
        Base.__init__(self, api)

    def _check_scheduled_for_range(self, scheduled_for_range):
        for s in scheduled_for_range:
            if not is_valid_datetime(s, "%Y-%m-%d"):
                return False
        return True

    def get_orders_group(self, scheduled_for_range, statuses):
        if not self._check_scheduled_for_range(scheduled_for_range):
            raise ParamValueException("Invalid Scheduled Range")
        data = {
            "filters": {
                "scheduled_for_range": scheduled_for_range,
                "statuses": statuses,
            }
        }
        items = []
        try:
            response = self.api._make_request(
                ORDERS_GROUP_V5, self.params, self.api._request_post, json=data
            )
            data = response.json()
            if "data" in data.keys():
                items = data["data"].get("items", [])
            return items
        except APIException as e:
            return e.to_dict()
        except ValueError:
            return response.content

    def assign_optimization_profile(self, optimization_profile_id, group_id):
        data = {
            "group_id": group_id,
            "optimization_profile_id": optimization_profile_id,
        }
        try:
            response = self.api._make_request(
                ASSIGN_PROFILES_V5, self.params, self.api._request_post, json=data
            )
            data = response.json()
            return data
        except APIException as e:
            return e.to_dict()
        except ValueError:
            return response.content
