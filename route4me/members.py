import json

from route4me.api_endpoints import (
    MEMBER_AUTHENTICATE,
    USER_LICENSE_HOST,
    VALIDATE_SESSION,
    WEBINAR_REGISTER,
    VERIFY_DEVICE_LICENSE,
    GET_USERS_HOST,
    USER_URL,
    REGISTER_ACTION
)
from route4me.base import Base
from route4me.exceptions import ParamValueException


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
            data = json.dumps(kwargs, ensure_ascii=False)
            response = self.api._request_post(USER_LICENSE_HOST,
                                              self.params,
                                              data=data)
            try:
                return json.loads(response.content)
            except ValueError:
                return response.content
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
            data = json.dumps(kwargs, ensure_ascii=False)
            response = self.api._request_post(VERIFY_DEVICE_LICENSE,
                                              self.params,
                                              data=data)
            try:
                return json.loads(response.content)
            except ValueError:
                return response.content
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
            response = self.api._request_post(MEMBER_AUTHENTICATE,
                                              self.params,
                                              data=kwargs)
            try:
                return json.loads(response.content)
            except ValueError:
                return response.content
        else:
            raise ParamValueException('order', 'Missing required params')

    def get_users(self, **kwargs):
        """
        Get users using GET request
        :return: API response
        """
        kwargs.update({'api_key': self.params['api_key'], })
        response = self.api._request_get(GET_USERS_HOST,
                                         kwargs)
        try:
            return response.json()
        except ValueError:
            return response.content

    def get_api_key_users(self, **kwargs):
        """
        Get users taht belong to a given api_key using GET request
        :return: API response
        """
        kwargs.update({'api_key': self.params['api_key'], })
        response = self.api._request_get(USER_URL,
                                         kwargs)
        try:
            return response.json()
        except ValueError:
            return response.content

    def validate_session(self, **kwargs):
        """
        Validate Session
        :param kwargs:
        :return: API response content
        """
        kwargs.update({'api_key': self.params['api_key'], })
        if self.check_required_params(kwargs, ['session_guid',
                                               'member_id', ]):
            response = self.api._request_get(VALIDATE_SESSION,
                                             kwargs)
            try:
                return json.loads(response.content)
            except ValueError:
                return response.content
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
            response = self.api._request_post(WEBINAR_REGISTER,
                                              self.params,
                                              data=kwargs)
            try:
                return json.loads(response.content)
            except ValueError:
                return response.content
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
            response = self.api._request_post(REGISTER_ACTION,
                                              params,
                                              data=kwargs)
            try:
                return response.json()
            except ValueError:
                return response.content
        else:
            raise ParamValueException('order', 'Missing required params')
