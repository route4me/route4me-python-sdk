# -*- coding: utf-8 -*-

from datetime import datetime
from .base import Base
from .api_endpoints import ROUTE_STATUS_V5
from .exceptions import APIException


class RouteStatus(Base):
    """
    Route Status

     - Planned
     - Started
     - Paused
     - Resumed
     - Completed


    """

    def __init__(self, api):
        """
        Routes
        :param api: Route4Me API Instance
        """
        self.params = {'api_key': api.key, }
        Base.__init__(self, api)

    def get_route_status(self, route_id):
        try:
            response = self.api._make_request("{}/{}".format(ROUTE_STATUS_V5, route_id),
                                              self.params,
                                              self.api._request_get)
            return response.json()
        except APIException as e:
            return e.to_dict()

    def get_route_status_history(self, route_id):
        try:
            response = self.api._make_request("{}/{}/history".format(ROUTE_STATUS_V5, route_id),
                                              self.params,
                                              self.api._request_get)
            return response.json()
        except APIException as e:
            return e.to_dict()

    def set_route_status(self, route_id, status, lat, lng, event_timestamp=None):
        if event_timestamp is None:
            event_timestamp = int(datetime.now().timestamp())
        data = {
            "status": status,
            "lat": lat,
            'lng': lng,
            'event_timestamp': event_timestamp,
        }
        try:
            response = self.api._make_request("{}/{}".format(ROUTE_STATUS_V5, route_id),
                                              self.params,
                                              self.api._request_post,
                                              json=data)
            return response.json()
        except APIException as e:
            return e.to_dict()

    def rollback_route_status(self, route_id):
        try:
            response = self.api._make_request("{}/{}/rollback".format(ROUTE_STATUS_V5, route_id),
                                              self.params,
                                              self.api._request_get)
            return response.json()
        except APIException as e:
            return e.to_dict()
