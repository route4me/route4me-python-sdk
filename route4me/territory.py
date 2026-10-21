from .api_endpoints import TERRITORY_HOST
from .base import Base
from .exceptions import ParamValueException


class Territory(Base):
    """
    Territory Management
    """

    def __init__(self, api):
        self.json_data = {}
        Base.__init__(self, api)

    def get_territories(self):
        return self._call_api(TERRITORY_HOST, "get", self.params, required=["api_key"])

    def get_territory(self, **kwargs):
        kwargs.update({"api_key": self.params["api_key"]})
        return self._call_api(TERRITORY_HOST, "get", kwargs, required=["api_key", "territory_id"])

    def add_territory(self, **kwargs):
        if not self.check_required_params(kwargs, ["territory_name", "territory_color", "territory"]):
            raise ParamValueException("params", "Params are not complete")
        return self._call_api(TERRITORY_HOST, "post", self.params, body=kwargs)

    def delete_territory(self, **kwargs):
        kwargs.update({"api_key": self.params["api_key"]})
        return self._call_api(TERRITORY_HOST, "delete", kwargs, required=["territory_id"])

    def update_territory(self, territory_id, **kwargs):
        self.params.update({"territory_id": territory_id})
        if not self.check_required_params(kwargs, ["territory_name", "territory_color", "territory"]):
            raise ParamValueException("params", "Params are not complete")
        return self._call_api(TERRITORY_HOST, "put", self.params, body=kwargs)
