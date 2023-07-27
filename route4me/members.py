# -*- coding: utf-8 -*-

import json
from .exceptions import APIException

from .api_endpoints import (
    MEMBER_AUTHENTICATE,
    USER_LICENSE_HOST,
    VALIDATE_SESSION,
    WEBINAR_REGISTER,
    VERIFY_DEVICE_LICENSE,
    GET_USERS_HOST,
    USER_URL,
    REGISTER_ACTION
)
from .base import Base
from .exceptions import ParamValueException


class Members(Base):
    """
    Members management.
    """

    def __init__(self, api):
        """
        Members Instance
        :param api:
        :return:
        """
        Base.__init__(self, api)

    def app_purchase_user_license(self, **kwargs):
        """
        Application purchase user License
        :param kwargs:
        :return: API response content
        """
        if self.check_required_params(kwargs, ['member_id',
                                               'session_guid',
                                               'device_id',
                                               'device_type',
                                               'subscription_name',
                                               'token',
                                               'payload',
                                               'format', ]):
            try:
                response = self.api._make_request(USER_LICENSE_HOST,
                                                  self.params,
                                                  self.api._request_post,
                                                  json=kwargs)
                try:
                    return json.loads(response.content)
                except ValueError:
                    return response.content
            except APIException as e:
                return e.to_dict()
        else:
            raise ParamValueException('order', 'Missing required params')

    def verify_device_license(self, **kwargs):
        """
        Verify User License
        :param kwargs:
        :return: API response content
        """
        if self.check_required_params(kwargs, ['device_id',
                                               'device_type',
                                               'format', ]):
            try:
                response = self.api._make_request(VERIFY_DEVICE_LICENSE,
                                                  self.params,
                                                  self.api._request_post,
                                                  json=kwargs)
                try:
                    return json.loads(response.content)
                except ValueError:
                    return response.content
            except APIException as e:
                return e.to_dict()
        else:
            raise ParamValueException('order', 'Missing required params')

    def member_authenticate(self, **kwargs):
        """
        Member Authenticate
        :param kwargs:
        :return: API response content
        """
        if self.check_required_params(kwargs, ['email',
                                               'password', ]):
            kwargs['strEmail'] = kwargs.pop('email')
            kwargs['strPassword'] = kwargs.pop('password')
            try:
                response = self.api._make_request(MEMBER_AUTHENTICATE,
                                                  self.params,
                                                  self.api._request_post,
                                                  json=kwargs)
                try:
                    return json.loads(response.content)
                except ValueError:
                    return response.content
            except APIException as e:
                return e.to_dict()
        else:
            raise ParamValueException('order', 'Missing required params')

    def get_users(self, **kwargs):
        """
        Get users using GET request
        :return: API response
        """
        kwargs.update({'api_key': self.params['api_key'], })
        try:
            response = self.api._make_request(GET_USERS_HOST,
                                              kwargs,
                                              self.api._request_get)
            try:
                return response.json()
            except ValueError:
                return response.content
        except APIException as e:
            return e.to_dict()

    def get_api_key_users(self, **kwargs):
        """
        Get users that belong to a given api_key using GET request
        :return: API response
        """
        kwargs.update({'api_key': self.params['api_key'], })
        try:
            response = self.api._make_request(USER_URL,
                                              kwargs,
                                              self.api._request_get)
            try:
                return response.json()
            except ValueError:
                return response.content
        except APIException as e:
            return e.to_dict()

    def validate_session(self, **kwargs):
        """
        Validate Session
        :param kwargs:
        :return: API response content
        """
        kwargs.update({'api_key': self.params['api_key'], })
        if self.check_required_params(kwargs, ['session_guid',
                                               'member_id', ]):
            try:
                response = self.api._make_request(VALIDATE_SESSION,
                                                  kwargs,
                                                  self.api._request_get)
                try:
                    return json.loads(response.content)
                except ValueError:
                    return response.content
            except APIException as e:
                return e.to_dict()
        else:
            raise ParamValueException('order', 'Missing required params')

    def webinar_registration(self, **kwargs):
        """
        Webinar Register
        :param kwargs:
        :return: API response content
        """
        if self.check_required_params(kwargs, ["email_address",
                                               "first_name",
                                               "last_name",
                                               "phone_number",
                                               "company_name",
                                               "member_id",
                                               "webiinar_date"]):
            try:
                response = self.api._make_request(WEBINAR_REGISTER,
                                                  self.params,
                                                  self.api._request_post,
                                                  data=kwargs)
                try:
                    return json.loads(response.content)
                except ValueError:
                    return response.content
            except APIException as e:
                return e.to_dict()
        else:
            raise ParamValueException('order', 'Missing required params')

    def register(self, **kwargs):
        """
        Register Action
        :param kwargs:
        :return: API response content
        """
        if self.check_required_params(kwargs, ["industry",
                                               "first_name",
                                               "last_name",
                                               "email_address",
                                               "check_terms",
                                               "device_type",
                                               "plan",
                                               "password_1",
                                               "password_2",
                                               "format"]):
            params = {'plan': kwargs.pop('plan')}
            kwargs['strIndustry'] = kwargs.pop('industry')
            kwargs['strFirstName'] = kwargs.pop('first_name')
            kwargs['strLastName'] = kwargs.pop('last_name')
            kwargs['strEmail'] = kwargs.pop('email_address')
            kwargs['chkTerms'] = kwargs.pop('check_terms')
            kwargs['device_type'] = kwargs.pop('device_type')
            kwargs['strPassword_1'] = kwargs.pop('password_1')
            kwargs['strPassword_2'] = kwargs.pop('password_2')
            try:
                response = self.api._make_request(REGISTER_ACTION,
                                                  params,
                                                  self.api._request_post,
                                                  data=kwargs)
                try:
                    return response.json()
                except ValueError:
                    return response.content
            except APIException as e:
                return e.to_dict()
        else:
            raise ParamValueException('order', 'Missing required params')
