from ._api_method import make_request
from .api_endpoints import ACTIVITY_FEED
from .base import Base
from .exceptions import ParamValueException


class ActivityFeed(Base):
    """
    Activity Feed Management
    """

    def __init__(self, api):
        self.json_data = {}
        Base.__init__(self, api)

    def get_activities_feed(self, **kwargs):
        kwargs.update({"api_key": self.params["api_key"]})
        return make_request(self, ACTIVITY_FEED, "get", kwargs, required=["api_key"])

    def get_activities_feed_by_type(self, **kwargs):
        kwargs.update({"api_key": self.params["api_key"]})
        return make_request(self, ACTIVITY_FEED, "get", kwargs, required=["api_key", "activity_type"])

    def get_activity_feed_inserted(self, **kwargs):
        kwargs.update({"api_key": self.params["api_key"], "activity_type": "insert-destination"})
        return make_request(self, ACTIVITY_FEED, "get", kwargs, required=["api_key", "route_id"])

    def get_activity_feed_deleted(self, **kwargs):
        kwargs.update({"api_key": self.params["api_key"], "activity_type": "delete-destination"})
        return make_request(self, ACTIVITY_FEED, "get", kwargs, required=["api_key", "route_id"])

    def get_activity_feed_route_owner_changed(self, **kwargs):
        kwargs.update({"api_key": self.params["api_key"], "activity_type": "route-owner-changed"})
        return make_request(self, ACTIVITY_FEED, "get", kwargs, required=["api_key", "route_id"])

    def log_specific_message(self, **kwargs):
        self.json_data = kwargs
        kwargs.update({"api_key": self.params["api_key"], "activity_type": "user_message"})
        if not self.check_required_params(self.json_data, ["api_key", "activity_message", "route_id"]):
            raise ParamValueException("params", "Params are not complete")
        return make_request(self, ACTIVITY_FEED, "post", self.params, body=self.json_data)
