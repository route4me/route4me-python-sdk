"""The :class:`OptimizationProfiles` resource (API V5): list optimization profiles."""

from .api_endpoints import OPTIMIZATION_PROFILES_V5
from .base import Base
from .exceptions import APIException


class OptimizationProfiles(Base):
    """Optimization profiles: saved optimization settings (API V5).

    Use it as ``route4me.optimization_profiles``. Requests go to
    ``wh.route4me.com``.
    """

    def __init__(self, api):
        """Create the resource.

        :param api: the :class:`~route4me.api.Route4Me` client.
        """
        Base.__init__(self, api)

    def get_optimization_profiles(self):
        """List the optimization profiles.

        Sends ``GET /modules/api/v5.0/optimization-profiles/data-list``.

        :return: the decoded JSON reply, the raw body (``bytes``) when it is
            not JSON, or the ``{"errors": ...}`` dict on an API error.
        """
        try:
            response = self._request(OPTIMIZATION_PROFILES_V5, self.params, "get")
            data = response.json()
            return data
        except APIException as e:
            return e.to_dict()
        except ValueError:
            return response.content
