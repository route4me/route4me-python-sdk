from ._url import join_path, path_int, path_segment
from .api_endpoints import RAPID_ADDRESS, RAPID_ADDRESS_SERVICE, RAPID_ADDRESS_ZIP
from .base import Base
from .exceptions import APIException, ParamValueException


class RapidAddress(Base):
    """
    Rapid Address is a service to get Street Addresses given
    Street name or Zip code

    .. versionchanged:: 0.2.0
       Path components are percent-encoded and validated. They were previously
       interpolated raw, so a value containing ``/``, ``?``, ``#`` or ``..``
       rewrote the request path against ``rapid.route4me.com``.

       ``get_street_data`` now issues a request on every branch. It used to
       build a URL for the ``offset``/``limit`` case and then fall off the end
       of the function, returning ``None`` without ever calling the API.
    """

    def __init__(self, api):
        """
        Address Instance
        :param api:
        :return:
        """
        Base.__init__(self, api)

    def _get(self, url, params):
        """Issue a GET and normalise the outcome.

        ``response`` is only referenced after a successful assignment. The
        previous inline version wrapped the request itself in
        ``except ValueError: return response.content``, so when
        ``_make_request`` raised before the assignment the handler died with
        ``UnboundLocalError`` and hid the real error.
        """
        try:
            response = self.api._make_request(url, params, self.api._request_get)
        except APIException as e:
            return e.to_dict()
        try:
            return response.json()
        except ValueError:
            return response.content

    @staticmethod
    def _paginated(url, kwargs):
        """Append ``offset``/``limit`` path components when both are supplied."""
        if "offset" in kwargs and "limit" in kwargs:
            return join_path(
                url,
                path_int(kwargs.pop("offset"), "offset"),
                path_int(kwargs.pop("limit"), "limit"),
            )
        return url

    def get_street_data(self, **kwargs):
        """
        Get Street Data
        :param kwargs: optional ``pk``, or ``offset`` and ``limit``
        :return: API response content
        """
        kwargs.update({"api_key": self.params["api_key"]})
        url = RAPID_ADDRESS
        if "offset" in kwargs and "limit" in kwargs:
            url = self._paginated(url, kwargs)
        elif "pk" in kwargs:
            url = join_path(url, path_segment(kwargs.pop("pk"), "pk"))
        return self._get(url, kwargs)

    def get_street_data_zip(self, **kwargs):
        """
        Get Street Data Given Zipcode
        :param kwargs: requires ``zipcode``; optional ``offset`` and ``limit``
        :return: API response content
        """
        kwargs.update({"api_key": self.params["api_key"]})
        if not self.check_required_params(kwargs, ["zipcode", "api_key"]):
            raise ParamValueException("params", "Params are not complete")
        url = join_path(RAPID_ADDRESS_ZIP, path_segment(kwargs.pop("zipcode"), "zipcode"))
        url = self._paginated(url, kwargs)
        return self._get(url, kwargs)

    def get_street_data_service(self, **kwargs):
        """
        Get Street Data Given Zipcode and House Number
        :param kwargs: requires ``zipcode`` and ``housenumber``; optional
            ``offset`` and ``limit``
        :return: API response content
        """
        kwargs.update({"api_key": self.params["api_key"]})
        if not self.check_required_params(kwargs, ["zipcode", "api_key", "housenumber"]):
            raise ParamValueException("params", "Params are not complete")
        url = join_path(
            RAPID_ADDRESS_SERVICE,
            path_segment(kwargs.pop("zipcode"), "zipcode"),
            path_segment(kwargs.pop("housenumber"), "housenumber"),
        )
        url = self._paginated(url, kwargs)
        return self._get(url, kwargs)
