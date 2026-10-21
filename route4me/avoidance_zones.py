from .api_endpoints import AVOIDANCE
from .base import Base
from .exceptions import ParamValueException


class AvoidanceZones(Base):
    """
    Avoidance Zones Management
    """

    def __init__(self, api):
        self.json_data = {}
        Base.__init__(self, api)

    def get_avoidance_zones(self):
        return self._call_api(AVOIDANCE, "get", self.params, required=["api_key"])

    def get_avoidance_zone(self, **kwargs):
        kwargs.update({"api_key": self.params["api_key"]})
        return self._call_api(AVOIDANCE, "get", kwargs, required=["api_key", "territory_id"])

    def add_avoidance_zone(self, **kwargs):
        if not self.check_required_params(kwargs, ["territory_name", "territory_color", "territory"]):
            raise ParamValueException("params", "Params are not complete")
        return self._call_api(AVOIDANCE, "post", self.params, body=kwargs)

    def delete_avoidance_zone(self, **kwargs):
        kwargs.update({"api_key": self.params["api_key"]})
        return self._call_api(AVOIDANCE, "delete", kwargs, required=["territory_id"])

    def update_avoidance_zone(self, territory_id, **kwargs):
        self.params.update({"territory_id": territory_id})
        if not self.check_required_params(kwargs, ["territory_name", "territory_color", "territory"]):
            raise ParamValueException("params", "Params are not complete")
        return self._call_api(AVOIDANCE, "put", self.params, body=kwargs)


# Backward-compatible alias for the old misspelled name
AvoindanceZones = AvoidanceZones
