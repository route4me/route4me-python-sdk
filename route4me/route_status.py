# -*- coding: utf-8 -*-

from datetime import datetime
from .base import Base
from .api_endpoints import ROUTE_STATUS_V5


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
        response = self.api._request_get("{}/{}".format(ROUTE_STATUS_V5, route_id),
                                         self.params)
        return response.json()

    def get_route_status_history(self, route_id):
        response = self.api._request_get("{}/{}/history".format(ROUTE_STATUS_V5, route_id),
                                         self.params)
        return response.json()

    def set_route_status(self, route_id, status, lat, lng, event_timestamp=None):
        if event_timestamp is None:
            event_timestamp = int(datetime.now().timestamp())
        data = {
            "status": status,
            "lat": lat,
            'lng': lng,
            'event_timestamp': event_timestamp,
        }
        response = self.api._request_post("{}/{}".format(ROUTE_STATUS_V5, route_id),
                                          self.params,
                                          json=data)
        return response.json()

    def rollback_route_status(self, route_id):
        response = self.api._request_get("{}/{}/rollback".format(ROUTE_STATUS_V5, route_id),
                                         self.params)
        return response.json()
