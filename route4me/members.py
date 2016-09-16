import json
from .base import Base
from .exceptions import ParamValueException
from .utils import json2obj


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
            response = self.api._request_post(self.api.user_license_url(),
                                              self.params,
                                              data=json.dumps(kwargs, ensure_ascii=False))
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
            response = self.api._request_post(self.api.verify_device_license_url(),
                                              self.params,
                                              data=json.dumps(kwargs, ensure_ascii=False))
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
            response = self.api._request_post(self.api.member_authenticate_url(),
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
        response = self.api._request_get(self.api.get_users_host_url(),
                                         kwargs)
        try:
            return json2obj(response.content)
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
            response = self.api._request_get(self.api.validate_session_url(),
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
            response = self.api._request_post(self.api.webinar_register_url(),
                                              self.params,
                                              data=kwargs)
            try:
                return json.loads(response.content)
            except ValueError:
                return response.content
        else:
            raise ParamValueException('order', 'Missing required params')
