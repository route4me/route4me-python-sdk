"""The :class:`RapidAddress` resource: street data by ID, zip code or house number."""

import warnings

from ._url import join_path, path_int, path_segment
from .api_endpoints import RAPID_ADDRESS, RAPID_ADDRESS_SERVICE, RAPID_ADDRESS_ZIP
from .base import Base
from .exceptions import ParamValueException


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

    Use it as ``route4me.rapid_address``. The methods send no request: the
    street-data endpoints on ``rapid.route4me.com`` are gone, and the SDK
    does not send the API key to an endpoint that no longer exists. Each
    method still checks its arguments, warns, and returns the
    ``{"errors": ...}`` dict.

    .. versionchanged:: 1.0.0
       The methods no longer send a request. Before, every request returned
       404, after sending the API key in the query string.
    """

    def __init__(self, api):
        """Create the resource.

        :param api: the :class:`~route4me.api.Route4Me` client.
        """
        Base.__init__(self, api)

    @staticmethod
    def _gone():
        """Return the error dict of a street-data method, which sends no request.

        :return: ``{"errors": [...]}``.
        """
        return {"errors": ["rapid.route4me.com no longer serves /street_data, so no request was sent."]}

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

        Sends no request: ``rapid.route4me.com`` no longer serves
        ``/street_data``.

        :param kwargs: optional ``pk``, the ID of one record, or ``offset``
            and ``limit`` for one page; they are checked, then ignored.
        :return: the ``{"errors": ...}`` dict.
        :raise ParamValueException: when ``offset`` or ``limit`` is not a
            non-negative integer, or ``pk`` is empty.

        .. deprecated:: 1.0.0
           ``rapid.route4me.com`` no longer serves ``/street_data``: every
           request returns 404. There is no replacement in the API.
        """
        _warn_retired("get_street_data")
        if "offset" in kwargs and "limit" in kwargs:
            self._paginated(RAPID_ADDRESS, kwargs)
        elif "pk" in kwargs:
            path_segment(kwargs.pop("pk"), "pk")
        return self._gone()

    def get_street_data_zip(self, **kwargs):
        """Get the street data of a zip code.

        Sends no request: ``rapid.route4me.com`` no longer serves
        ``/street_data``.

        :param kwargs: requires ``zipcode``; optional ``offset`` and
            ``limit``. They are checked, then ignored.
        :return: the ``{"errors": ...}`` dict.
        :raise ParamValueException: when ``zipcode`` is missing or empty, or
            ``offset`` or ``limit`` is not a non-negative integer.

        .. deprecated:: 1.0.0
           ``rapid.route4me.com`` no longer serves ``/street_data``: every
           request returns 404. There is no replacement in the API.
        """
        _warn_retired("get_street_data_zip")
        if not self.check_required_params(kwargs, ["zipcode"]):
            raise ParamValueException("params", "Params are not complete")
        url = join_path(RAPID_ADDRESS_ZIP, path_segment(kwargs.pop("zipcode"), "zipcode"))
        self._paginated(url, kwargs)
        return self._gone()

    def get_street_data_service(self, **kwargs):
        """Get the street data of a house number in a zip code.

        Sends no request: ``rapid.route4me.com`` no longer serves
        ``/street_data``.

        :param kwargs: requires ``zipcode`` and ``housenumber``; optional
            ``offset`` and ``limit``. They are checked, then ignored.
        :return: the ``{"errors": ...}`` dict.
        :raise ParamValueException: when ``zipcode`` or ``housenumber`` is
            missing or empty, or ``offset`` or ``limit`` is not a non-negative
            integer.

        .. deprecated:: 1.0.0
           ``rapid.route4me.com`` no longer serves ``/street_data``: every
           request returns 404. There is no replacement in the API.
        """
        _warn_retired("get_street_data_service")
        if not self.check_required_params(kwargs, ["zipcode", "housenumber"]):
            raise ParamValueException("params", "Params are not complete")
        url = join_path(
            RAPID_ADDRESS_SERVICE,
            path_segment(kwargs.pop("zipcode"), "zipcode"),
            path_segment(kwargs.pop("housenumber"), "housenumber"),
        )
        self._paginated(url, kwargs)
        return self._gone()
