"""The :class:`ActivityFeed` resource: read the activity feed and log messages to it."""

from .api_endpoints import ACTIVITY_FEED
from .base import Base
from .exceptions import ParamValueException


class ActivityFeed(Base):
    """Activity feed: the events recorded on routes and in the account.

    Use it as ``route4me.activity_feed``. Every method sends a request to
    ``/api.v4/activity_feed.php``.

    Unless stated otherwise, a method returns the decoded JSON reply, or on an
    API error the ``{"errors": ...}`` dict from :meth:`APIException.to_dict
    <route4me.exceptions.APIException.to_dict>` instead of raising.
    """

    def __init__(self, api):
        self.json_data = {}
        Base.__init__(self, api)

    def get_activities_feed(self, **kwargs):
        """Get activities from the feed.

        Sends ``GET /api.v4/activity_feed.php``.

        :param kwargs: query parameters, sent as is, e.g. ``limit`` and
            ``offset``.
        :return: the decoded JSON reply: the activities, or the
            ``{"errors": ...}`` dict on an API error.
        """
        kwargs.update({"api_key": self.params["api_key"]})
        return self._call_api(ACTIVITY_FEED, "get", kwargs, required=["api_key"])

    def get_activities_feed_by_type(self, **kwargs):
        """Get the activities of one type.

        Sends ``GET /api.v4/activity_feed.php``.

        :param kwargs: query parameters. Required: ``activity_type``, e.g.
            ``"insert-destination"``.
        :return: the decoded JSON reply: the activities, or the
            ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when ``activity_type`` is missing.
        """
        kwargs.update({"api_key": self.params["api_key"]})
        return self._call_api(ACTIVITY_FEED, "get", kwargs, required=["api_key", "activity_type"])

    def get_activity_feed_inserted(self, **kwargs):
        """Get the destinations inserted into a route.

        Sends ``GET /api.v4/activity_feed.php`` with
        ``activity_type=insert-destination``.

        :param kwargs: query parameters. Required: ``route_id``.
        :return: the decoded JSON reply: the activities, or the
            ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when ``route_id`` is missing.
        """
        kwargs.update({"api_key": self.params["api_key"], "activity_type": "insert-destination"})
        return self._call_api(ACTIVITY_FEED, "get", kwargs, required=["api_key", "route_id"])

    def get_activity_feed_deleted(self, **kwargs):
        """Get the destinations deleted from a route.

        Sends ``GET /api.v4/activity_feed.php`` with
        ``activity_type=delete-destination``.

        :param kwargs: query parameters. Required: ``route_id``.
        :return: the decoded JSON reply: the activities, or the
            ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when ``route_id`` is missing.
        """
        kwargs.update({"api_key": self.params["api_key"], "activity_type": "delete-destination"})
        return self._call_api(ACTIVITY_FEED, "get", kwargs, required=["api_key", "route_id"])

    def get_activity_feed_route_owner_changed(self, **kwargs):
        """Get the owner changes of a route.

        Sends ``GET /api.v4/activity_feed.php`` with
        ``activity_type=route-owner-changed``.

        :param kwargs: query parameters. Required: ``route_id``.
        :return: the decoded JSON reply: the activities, or the
            ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when ``route_id`` is missing.
        """
        kwargs.update({"api_key": self.params["api_key"], "activity_type": "route-owner-changed"})
        return self._call_api(ACTIVITY_FEED, "get", kwargs, required=["api_key", "route_id"])

    def log_specific_message(self, **kwargs):
        """Log a message on a route's activity feed.

        Sends ``POST /api.v4/activity_feed.php`` with the keywords and
        ``activity_type="user_message"`` as the JSON body.

        :param kwargs: required: ``route_id`` and ``activity_message``, the
            text to log.
        :return: the decoded JSON reply, or the ``{"errors": ...}`` dict on an
            API error.
        :raise ParamValueException: when a required parameter is missing.

        .. versionchanged:: 1.0.0
           The API key is no longer copied into the request body.
        """
        if not self.check_required_params(kwargs, ["activity_message", "route_id"]):
            raise ParamValueException("params", "Params are not complete")
        self.json_data = dict(kwargs, activity_type="user_message")
        return self._call_api(ACTIVITY_FEED, "post", self.params, body=self.json_data)
