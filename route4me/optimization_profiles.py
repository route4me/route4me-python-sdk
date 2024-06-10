# -*- coding: utf-8 -*-
from .base import Base
from .exceptions import APIException

from .api_endpoints import OPTIMIZATION_PROFILES_V5


class OptimizationProfiles(Base):

    def __init__(self, api):
        """
        Optimization Profile Instance
        :param api:
        :return:
        """
        Base.__init__(self, api)

    def get_optimization_profiles(self):
        try:
            response = self.api._make_request(
                OPTIMIZATION_PROFILES_V5, self.params, self.api._request_get
            )
            data = response.json()
            return data
        except APIException as e:
            print(response.content)
            return e.to_dict()
        except ValueError:
            return response.content
