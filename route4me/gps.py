from ._api_method import make_request
from .api_endpoints import DEVICE_LOCATION_URL, SET_GPS_HOST
from .base import Base


class GPS(Base):
    """
    Set GPS position of the device
    """

    requirements = (
        "api_key",
        "format",
        "member_id",
        "route_id",
        "course",
        "speed",
        "lat",
        "lng",
        "device_type",
        "device_guid",
        "device_timestamp",
    )

    def __init__(self, api):
        self.response = None
        self.params = {"api_key": api.key}
        Base.__init__(self, api)

    def set_gps_track(self, **kwargs):
        kwargs.update(self.params)
        return make_request(self, SET_GPS_HOST, "get", kwargs, required=self.requirements)

    def get_locations(self, **kwargs):
        kwargs.update({"api_key": self.params["api_key"]})
        return make_request(
            self,
            DEVICE_LOCATION_URL,
            "get",
            kwargs,
            required=["api_key", "format", "route_id", "member_id", "time_period"],
        )
