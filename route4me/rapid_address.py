"""The :class:`RapidAddress` resource: street data by ID, zip code or house number."""

import warnings

from ._url import join_path, path_int, path_segment
from .api_endpoints import RAPID_ADDRESS, RAPID_ADDRESS_SERVICE, RAPID_ADDRESS_ZIP
from .base import Base
from .exceptions import APIException, ParamValueException


def _warn_retired(method):
    """Warn that a street-data method calls an endpoint the API no longer serves.

    :param method: name of the deprecated method.
    """
    warnings.warn(
        f"RapidAddress.{method} is deprecated: rapid.route4me.com/street_data returns 404 and has no replacement.",
        DeprecationWarning,
        stacklevel=3,
    )


class RapidAddress(Base):
    """Rapid Address: street addresses by ID, zip code or house number.

    .. deprecated:: 1.0.0
       The street-data endpoints are gone from the API (they return 404), so
       every method here warns. The class will be removed in 2.0.

    Use it as ``route4me.rapid_address``. Requests go to
    ``https://rapid.route4me.com/street_data/``; IDs, zip codes and house
    numbers become path segments, and ``offset`` and ``limit`` are appended
    to the path when both are given. Every method returns the decoded JSON
    reply, the raw body (``bytes``) when it is not JSON, or on an API error the
    ``{"errors": ...}`` dict from :meth:`APIException.to_dict
    <route4me.exceptions.APIException.to_dict>` instead of raising.

    .. versionchanged:: 0.2.0
       Path components are percent-encoded and validated. They were previously
       interpolated raw, so a value containing ``/``, ``?``, ``#`` or ``..``
       rewrote the request path against ``rapid.route4me.com``.

       ``get_street_data`` now issues a request on every branch. It used to
       build a URL for the ``offset``/``limit`` case and then fall off the end
       of the function, returning ``None`` without ever calling the API.
    """

    def __init__(self, api):
        """Create the resource.

        :param api: the :class:`~route4me.api.Route4Me` client.
        """
        Base.__init__(self, api)

    def _get(self, url, params):
        """Issue a GET and normalise the outcome.

        ``response`` is only referenced after a successful assignment. The
        previous inline version wrapped the request itself in
        ``except ValueError: return response.content``, so when
        ``_make_request`` raised before the assignment the handler died with
        ``UnboundLocalError`` and hid the real error.

        :param url: absolute URL to request.
        :param params: query parameters.
        :return: the decoded JSON reply, the raw body (``bytes``) when it is
            not JSON, or the ``{"errors": ...}`` dict on an API error.
        """
        try:
            response = self._request(url, params, "get")
        except APIException as e:
            return e.to_dict()
        try:
            return response.json()
        except ValueError:
            return response.content

    @staticmethod
    def _paginated(url, kwargs):
        """Append ``offset``/``limit`` path components when both are supplied.

        :param url: the URL to extend.
        :param kwargs: the method's keywords; ``offset`` and ``limit`` are
            removed from it when used.
        :return: the URL, extended or unchanged.
        :raise ParamValueException: when ``offset`` or ``limit`` is not a
            non-negative integer.
        """
        if "offset" in kwargs and "limit" in kwargs:
            return join_path(
                url,
                path_int(kwargs.pop("offset"), "offset"),
                path_int(kwargs.pop("limit"), "limit"),
            )
        return url

    def get_street_data(self, **kwargs):
        """Get street data: all of it, one page, or one record.

        Sends ``GET /street_data/``, ``GET /street_data/{offset}/{limit}/``
        or ``GET /street_data/{pk}/`` on ``rapid.route4me.com``.

        :param kwargs: optional ``pk``, the ID of one record, or ``offset``
            and ``limit`` for one page. Other keywords are sent as query
            parameters.
        :return: the decoded JSON reply, the raw body (``bytes``) when it is
            not JSON, or the ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when ``offset`` or ``limit`` is not a
            non-negative integer, or ``pk`` is empty.

        .. deprecated:: 1.0.0
           ``rapid.route4me.com`` no longer serves ``/street_data``: every
           request returns 404. There is no replacement in the API.
        """
        _warn_retired("get_street_data")
        kwargs.update({"api_key": self.params["api_key"]})
        url = RAPID_ADDRESS
        if "offset" in kwargs and "limit" in kwargs:
            url = self._paginated(url, kwargs)
        elif "pk" in kwargs:
            url = join_path(url, path_segment(kwargs.pop("pk"), "pk"))
        return self._get(url, kwargs)

    def get_street_data_zip(self, **kwargs):
        """Get the street data of a zip code.

        Sends ``GET /street_data/zipcode/{zipcode}/`` on
        ``rapid.route4me.com``, with ``{offset}/{limit}/`` appended when both
        are given.

        :param kwargs: requires ``zipcode``; optional ``offset`` and ``limit``.
        :return: the decoded JSON reply, the raw body (``bytes``) when it is
            not JSON, or the ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when ``zipcode`` is missing or empty, or
            ``offset`` or ``limit`` is not a non-negative integer.

        .. deprecated:: 1.0.0
           ``rapid.route4me.com`` no longer serves ``/street_data``: every
           request returns 404. There is no replacement in the API.
        """
        _warn_retired("get_street_data_zip")
        kwargs.update({"api_key": self.params["api_key"]})
        if not self.check_required_params(kwargs, ["zipcode", "api_key"]):
            raise ParamValueException("params", "Params are not complete")
        url = join_path(RAPID_ADDRESS_ZIP, path_segment(kwargs.pop("zipcode"), "zipcode"))
        url = self._paginated(url, kwargs)
        return self._get(url, kwargs)

    def get_street_data_service(self, **kwargs):
        """Get the street data of a house number in a zip code.

        Sends ``GET /street_data/service/{zipcode}/{housenumber}/`` on
        ``rapid.route4me.com``, with ``{offset}/{limit}/`` appended when both
        are given.

        :param kwargs: requires ``zipcode`` and ``housenumber``; optional
            ``offset`` and ``limit``.
        :return: the decoded JSON reply, the raw body (``bytes``) when it is
            not JSON, or the ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when ``zipcode`` or ``housenumber`` is
            missing or empty, or ``offset`` or ``limit`` is not a non-negative
            integer.

        .. deprecated:: 1.0.0
           ``rapid.route4me.com`` no longer serves ``/street_data``: every
           request returns 404. There is no replacement in the API.
        """
        _warn_retired("get_street_data_service")
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
