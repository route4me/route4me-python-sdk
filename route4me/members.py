from .api_endpoints import (
    GET_USERS_HOST,
    MEMBER_AUTHENTICATE,
    REGISTER_ACTION,
    USER_LICENSE_HOST,
    USER_URL,
    VALIDATE_SESSION,
    VERIFY_DEVICE_LICENSE,
    WEBINAR_REGISTER,
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
        if not self.check_required_params(
            kwargs,
            [
                "member_id",
                "session_guid",
                "device_id",
                "device_type",
                "subscription_name",
                "token",
                "payload",
                "format",
            ],
        ):
            raise ParamValueException("order", "Missing required params")
        return self._request_decoded(USER_LICENSE_HOST, self.params, "post", json=kwargs)

    def verify_device_license(self, **kwargs):
        """
        Verify User License
        :param kwargs:
        :return: API response content
        """
        if not self.check_required_params(
            kwargs,
            [
                "device_id",
                "device_type",
                "format",
            ],
        ):
            raise ParamValueException("order", "Missing required params")
        return self._request_decoded(VERIFY_DEVICE_LICENSE, self.params, "post", json=kwargs)

    def member_authenticate(self, **kwargs):
        """
        Member Authenticate
        :param kwargs:
        :return: API response content
        """
        if not self.check_required_params(
            kwargs,
            [
                "email",
                "password",
            ],
        ):
            raise ParamValueException("order", "Missing required params")
        kwargs["strEmail"] = kwargs.pop("email")
        kwargs["strPassword"] = kwargs.pop("password")
        return self._request_decoded(MEMBER_AUTHENTICATE, self.params, "post", json=kwargs)

    def get_users(self, **kwargs):
        """
        Get users using GET request
        :return: API response
        """
        kwargs.update(
            {
                "api_key": self.params["api_key"],
            }
        )
        return self._request_decoded(GET_USERS_HOST, kwargs, "get")

    def get_api_key_users(self, **kwargs):
        """
        Get users that belong to a given api_key using GET request
        :return: API response
        """
        kwargs.update(
            {
                "api_key": self.params["api_key"],
            }
        )
        return self._request_decoded(USER_URL, kwargs, "get")

    def validate_session(self, **kwargs):
        """
        Validate Session
        :param kwargs:
        :return: API response content
        """
        kwargs.update(
            {
                "api_key": self.params["api_key"],
            }
        )
        if not self.check_required_params(
            kwargs,
            [
                "session_guid",
                "member_id",
            ],
        ):
            raise ParamValueException("order", "Missing required params")
        return self._request_decoded(VALIDATE_SESSION, kwargs, "get")

    def webinar_registration(self, **kwargs):
        """
        Webinar Register
        :param kwargs:
        :return: API response content
        """
        if not self.check_required_params(
            kwargs,
            ["email_address", "first_name", "last_name", "phone_number", "company_name", "member_id", "webiinar_date"],
        ):
            raise ParamValueException("order", "Missing required params")
        return self._request_decoded(WEBINAR_REGISTER, self.params, "post", data=kwargs)

    def register(self, **kwargs):
        """
        Register Action
        :param kwargs:
        :return: API response content
        """
        if not self.check_required_params(
            kwargs,
            [
                "industry",
                "first_name",
                "last_name",
                "email_address",
                "check_terms",
                "device_type",
                "plan",
                "password_1",
                "password_2",
                "format",
            ],
        ):
            raise ParamValueException("order", "Missing required params")
        params = {"plan": kwargs.pop("plan")}
        kwargs["strIndustry"] = kwargs.pop("industry")
        kwargs["strFirstName"] = kwargs.pop("first_name")
        kwargs["strLastName"] = kwargs.pop("last_name")
        kwargs["strEmail"] = kwargs.pop("email_address")
        kwargs["chkTerms"] = kwargs.pop("check_terms")
        kwargs["device_type"] = kwargs.pop("device_type")
        kwargs["strPassword_1"] = kwargs.pop("password_1")
        kwargs["strPassword_2"] = kwargs.pop("password_2")
        return self._request_decoded(REGISTER_ACTION, params, "post", data=kwargs)
