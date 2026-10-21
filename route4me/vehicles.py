from .api_endpoints import VEHICLES_HOST
from .base import Base


class Vehicle(Base):
    """
    Vehicles Management
    """

    def __init__(self, api):
        self.json_data = {}
        Base.__init__(self, api)

    def get_vehicles(self):
        return self._call_api(VEHICLES_HOST, "get", self.params, required=["api_key"])
