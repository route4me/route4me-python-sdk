# -*- coding: utf-8 -*-

import json

from .api_endpoints import ACTIVITY_FEED
from .base import Base
from .exceptions import ParamValueException


class ActivityFeed(Base):
    """
    Activity Feed Management
    """

    def __init__(self, api):
        """
        Activity Feed Instance
        :param api:
        :return:
        """
        self.json_data = {}
        Base.__init__(self, api)

    def get_activities_feed(self, **kwargs):
        """
        Get Activity Feed using GET request
        :return: API response
        :raise: ParamValueException if required params are not present.
        """
        kwargs.update({'api_key': self.params['api_key'], })
        if self.check_required_params(kwargs, ['api_key', ]):
            self.response = self.api._request_get(ACTIVITY_FEED,
                                                  kwargs)
            return self.response.json()
        else:
            raise ParamValueException('params', 'Params are not complete')

    def get_activities_feed_by_type(self, **kwargs):
        """
        Get Activity Feed by Type using GET request
        :return: API response
        :raise: ParamValueException if required params are not present.
        """
        kwargs.update({'api_key': self.params['api_key'], })
        if self.check_required_params(kwargs, ['api_key', 'activity_type']):
            self.response = self.api._request_get(ACTIVITY_FEED,
                                                  kwargs)
            return self.response.json()
        else:
            raise ParamValueException('params', 'Params are not complete')

    def get_activity_feed_inserted(self, **kwargs):
        """
        Get Activity Feed Inserted using GET request
        :return: API response
        :raise: ParamValueException if required params are not present.
        """
        kwargs.update({'api_key': self.params['api_key'],
                       'activity_type': 'insert-destination', })
        if self.check_required_params(kwargs, ['api_key', 'route_id']):
            self.response = self.api._request_get(ACTIVITY_FEED,
                                                  kwargs)
            return self.response.json()
        else:
            raise ParamValueException('params', 'Params are not complete')

    def get_activity_feed_deleted(self, **kwargs):
        """
        Get Activity Feed Deleted using GET request
        :return: API response
        :raise: ParamValueException if required params are not present.
        """
        kwargs.update({'api_key': self.params['api_key'],
                       'activity_type': 'delete-destination', })
        if self.check_required_params(kwargs, ['api_key', 'route_id']):
            self.response = self.api._request_get(ACTIVITY_FEED,
                                                  kwargs)
            return self.response.json()
        else:
            raise ParamValueException('params', 'Params are not complete')

    def get_activity_feed_route_owner_changed(self, **kwargs):
        """
        Get Activity Feed Route Owner Changed using GET request
        :return: API response
        :raise: ParamValueException if required params are not present.
        """
        kwargs.update({'api_key': self.params['api_key'],
                       'activity_type': 'route-owner-changed', })
        if self.check_required_params(kwargs, ['api_key', 'route_id']):
            self.response = self.api._request_get(ACTIVITY_FEED,
                                                  kwargs)
            return self.response.json()
        else:
            raise ParamValueException('params', 'Params are not complete')

    def log_specific_message(self, **kwargs):
        """
        Activity Feed Log an Specific Message using POST request
        :return: API response
        :raise: ParamValueException if required params are not present.
        """
        self.json_data = kwargs
        kwargs.update({'api_key': self.params['api_key'],
                       'activity_type': 'user_message', })
        if self.check_required_params(self.json_data, ['api_key',
                                                       'activity_message',
                                                       'route_id']):
            data = json.dumps(self.json_data, ensure_ascii=False)
            self.response = self.api._request_post(ACTIVITY_FEED,
                                                   self.params, data=data)
            return self.response.json()
        else:
            raise ParamValueException('params', 'Params are not complete')
