"""The :class:`Vehicle` resource: list the account's vehicles."""

from .api_endpoints import VEHICLES_HOST
from .base import Base


class Vehicle(Base):
    """Vehicles of the account. Use it as ``route4me.vehicles``."""

    def __init__(self, api):
        self.json_data = {}
        Base.__init__(self, api)

    def get_vehicles(self):
        """List the vehicles.

        Sends ``GET /api/vehicles/view_vehicles.php``.

        :return: the decoded JSON reply: the vehicles, or the
            ``{"errors": ...}`` dict on an API error.
        """
        return self._call_api(VEHICLES_HOST, "get", self.params, required=["api_key"])
