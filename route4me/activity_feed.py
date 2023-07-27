# -*- coding: utf-8 -*-

from .api_endpoints import ACTIVITY_FEED
from .base import Base
from .exceptions import ParamValueException
from .exceptions import APIException


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
            try:
                self.response = self.api._make_request(ACTIVITY_FEED,
                                                       kwargs,
                                                       self.api._request_get)
                return self.response.json()
            except APIException as e:
                return e.to_dict()
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
            try:
                self.response = self.api._make_request(ACTIVITY_FEED,
                                                       kwargs,
                                                       self.api._request_get)
                return self.response.json()
            except APIException as e:
                return e.to_dict()
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
            try:
                self.response = self.api._make_request(ACTIVITY_FEED,
                                                       kwargs,
                                                       self.api._request_get)
                return self.response.json()
            except APIException as e:
                return e.to_dict()
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
            try:
                self.response = self.api._make_request(ACTIVITY_FEED,
                                                       kwargs,
                                                       self.api._request_get)
                return self.response.json()
            except APIException as e:
                return e.to_dict()
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
            try:
                self.response = self.api._make_request(ACTIVITY_FEED,
                                                       kwargs,
                                                       self.api._request_get)
                return self.response.json()
            except APIException as e:
                return e.to_dict()
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
            try:
                self.response = self.api._make_request(ACTIVITY_FEED,
                                                       self.params,
                                                       self.api._request_post,
                                                       json=self.json_data)
                return self.response.json()
            except APIException as e:
                return e.to_dict()
        else:
            raise ParamValueException('params', 'Params are not complete')
