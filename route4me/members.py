"""The :class:`Members` resource: users, sessions, licenses and registration."""

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
    """Members: the users of the account, their sessions and licenses.

    Use it as ``route4me.members``.

    Every method returns the decoded JSON reply, the raw body (``bytes``) when
    it is not JSON, or on an API error the ``{"errors": ...}`` dict from
    :meth:`APIException.to_dict <route4me.exceptions.APIException.to_dict>`
    instead of raising.
    """

    def __init__(self, api):
        """Create the resource.

        :param api: the :class:`~route4me.api.Route4Me` client.
        """
        Base.__init__(self, api)

    def app_purchase_user_license(self, **kwargs):
        """Record a user license purchased in a mobile app.

        Sends ``POST /api/member/user_license.php`` with the keywords as the
        JSON body.

        :param kwargs: required: ``member_id``, ``session_guid``,
            ``device_id``, ``device_type``, ``subscription_name``, ``token``,
            ``payload`` and ``format``.
        :return: the decoded JSON reply, the raw body (``bytes``) when it is
            not JSON, or the ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when a required parameter is missing.
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
        """Verify the license of a device.

        Sends ``POST /api/device/verify_device_license.php`` with the keywords
        as the JSON body.

        :param kwargs: required: ``device_id``, ``device_type`` and ``format``.
        :return: the decoded JSON reply, the raw body (``bytes``) when it is
            not JSON, or the ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when a required parameter is missing.
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
        """Authenticate a member with an email address and a password.

        Sends ``POST /actions/authenticate.php`` with the keywords as the JSON
        body; ``email`` and ``password`` are sent as ``strEmail`` and
        ``strPassword``.

        :param kwargs: required: ``email`` and ``password``.
        :return: the decoded JSON reply, the raw body (``bytes``) when it is
            not JSON, or the ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when a required parameter is missing.
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
        """List the users of the account.

        Sends ``GET /api/member/view_users.php``.

        :param kwargs: query parameters, sent as is.
        :return: the decoded JSON reply, the raw body (``bytes``) when it is
            not JSON, or the ``{"errors": ...}`` dict on an API error.
        """
        kwargs.update(
            {
                "api_key": self.params["api_key"],
            }
        )
        return self._request_decoded(GET_USERS_HOST, kwargs, "get")

    def get_api_key_users(self, **kwargs):
        """List the users that belong to the API key.

        Sends ``GET /api.v4/user.php``.

        :param kwargs: query parameters, sent as is.
        :return: the decoded JSON reply, the raw body (``bytes``) when it is
            not JSON, or the ``{"errors": ...}`` dict on an API error.
        """
        kwargs.update(
            {
                "api_key": self.params["api_key"],
            }
        )
        return self._request_decoded(USER_URL, kwargs, "get")

    def validate_session(self, **kwargs):
        """Check whether a member's session is valid.

        Sends ``GET /datafeed/session/validate_session.php``.

        :param kwargs: query parameters. Required: ``session_guid`` and
            ``member_id``.
        :return: the decoded JSON reply, the raw body (``bytes``) when it is
            not JSON, or the ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when a required parameter is missing.
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
        """Register a member for a webinar.

        Sends ``POST /actions/webinar_register.php`` with the keywords as form
        fields.

        :param kwargs: required: ``email_address``, ``first_name``,
            ``last_name``, ``phone_number``, ``company_name``, ``member_id``
            and ``webinar_date``.
        :return: the decoded JSON reply, the raw body (``bytes``) when it is
            not JSON, or the ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when a required parameter is missing.
        """
        if not self.check_required_params(
            kwargs,
            ["email_address", "first_name", "last_name", "phone_number", "company_name", "member_id", "webiinar_date"],
        ):
            raise ParamValueException("order", "Missing required params")
        return self._request_decoded(WEBINAR_REGISTER, self.params, "post", data=kwargs)

    def register(self, **kwargs):
        """Register a new account.

        Sends ``POST /actions/register_action.php`` with ``plan`` in the query
        and the other keywords as form fields. ``industry``, ``first_name``,
        ``last_name``, ``email_address``, ``check_terms``, ``password_1`` and
        ``password_2`` are sent as ``strIndustry``, ``strFirstName``,
        ``strLastName``, ``strEmail``, ``chkTerms``, ``strPassword_1`` and
        ``strPassword_2``.

        :param kwargs: required: ``industry``, ``first_name``, ``last_name``,
            ``email_address``, ``check_terms``, ``device_type``, ``plan``,
            ``password_1``, ``password_2`` and ``format``.
        :return: the decoded JSON reply, the raw body (``bytes``) when it is
            not JSON, or the ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when a required parameter is missing.
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
