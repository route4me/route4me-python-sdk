"""The :class:`DriverReviews` resource (API V5): the reviews customers leave for drivers, and their settings."""

from ._params import compact
from ._url import path_segment
from .api_endpoints import (
    DRIVER_REVIEW_SETTINGS_BY_MEMBER_V5,
    DRIVER_REVIEW_SETTINGS_UPLOAD_V5,
    DRIVER_REVIEWS_V5,
)
from .base import Base


class DriverReviews(Base):
    """Driver reviews: the rating and comment a customer gives a delivery (API V5).

    A review is tied to the tracking number of the stop. Use it as
    ``route4me.driver_reviews``. Every method sends a request to
    ``/modules/api/v5.0/driver-reviews`` on ``wh.route4me.com``.

    Every method returns the decoded JSON reply, or on an API error the
    ``{"errors": ...}`` dict from :meth:`APIException.to_dict
    <route4me.exceptions.APIException.to_dict>` instead of raising.

    .. versionadded:: 1.0.0
    """

    def __init__(self, api):
        """Create the resource.

        :param api: the :class:`~route4me.api.Route4Me` client.
        """
        Base.__init__(self, api)

    @staticmethod
    def _review_url(rating_id):
        """Build the URL of one review, with ``rating_id`` encoded as one path segment.

        :param rating_id: ID of the review.
        :return: the absolute URL.
        :raise ParamValueException: when ``rating_id`` is empty.
        """
        return f"{DRIVER_REVIEWS_V5}/{path_segment(rating_id, 'rating_id')}"

    def get_driver_review_list(self, *, rating=None, member_id=None, start=None, end=None, page=None, per_page=None):
        """List the driver reviews, one page at a time.

        Sends ``GET /modules/api/v5.0/driver-reviews`` with the given filters
        in the query.

        :param rating: only reviews with this rating, 1 to 5.
        :param member_id: only reviews of this driver.
        :param start: only reviews from this date on, as ``YYYY-MM-DD``.
        :param end: only reviews up to this date, as ``YYYY-MM-DD``.
        :param page: page number, from 1.
        :param per_page: reviews per page.
        :return: the decoded JSON reply, or the ``{"errors": ...}`` dict on an
            API error.

        .. versionadded:: 1.0.0
        """
        query = compact(rating=rating, member_id=member_id, start=start, end=end, page=page, per_page=per_page)
        return self._call_api(DRIVER_REVIEWS_V5, "get", query)

    def get_driver_review_by_id(self, rating_id):
        """Get one driver review.

        Sends ``GET /modules/api/v5.0/driver-reviews/{rating_id}``.

        :param rating_id: ID of the review.
        :return: the decoded JSON reply, or the ``{"errors": ...}`` dict on an
            API error.
        :raise ParamValueException: when ``rating_id`` is empty.

        .. versionadded:: 1.0.0
        """
        return self._call_api(self._review_url(rating_id), "get", {})

    def create_driver_review(self, **fields):
        """Add a driver review.

        Sends ``POST /modules/api/v5.0/driver-reviews`` with the keywords as
        the JSON body.

        :param fields: the review: ``tracking_number``, the tracking number
            of the stop; ``rating``, 1 to 5; and ``review``, the comment.
        :return: the decoded JSON reply, or the ``{"errors": ...}`` dict on an
            API error.

        .. versionadded:: 1.0.0
        """
        return self._call_api(DRIVER_REVIEWS_V5, "post", {}, body=fields)

    def update_driver_review(self, rating_id, **fields):
        """Change some fields of a driver review.

        Sends ``PATCH /modules/api/v5.0/driver-reviews/{rating_id}`` with the
        keywords as the JSON body. :meth:`replace_driver_review` sends the
        same body with ``PUT``.

        :param rating_id: ID of the review.
        :param fields: the fields to change: ``tracking_number``, ``rating``
            or ``review``.
        :return: the decoded JSON reply, or the ``{"errors": ...}`` dict on an
            API error.
        :raise ParamValueException: when ``rating_id`` is empty.

        .. versionadded:: 1.0.0
        """
        return self._call_api(self._review_url(rating_id), "patch", {}, body=fields)

    def replace_driver_review(self, rating_id, **fields):
        """Replace a driver review.

        Sends ``PUT /modules/api/v5.0/driver-reviews/{rating_id}`` with the
        keywords as the JSON body.

        :param rating_id: ID of the review.
        :param fields: the review: ``tracking_number``, ``rating`` and
            ``review``.
        :return: the decoded JSON reply, or the ``{"errors": ...}`` dict on an
            API error.
        :raise ParamValueException: when ``rating_id`` is empty.

        .. versionadded:: 1.0.0
        """
        return self._call_api(self._review_url(rating_id), "put", {}, body=fields)

    def get_driver_review_settings_by_member(self):
        """Get the review settings of the authenticated member.

        Sends ``GET /modules/api/v5.0/driver-reviews/settings/get-by-member``.

        :return: the decoded JSON reply, or the ``{"errors": ...}`` dict on an
            API error.

        .. versionadded:: 1.0.0
        """
        return self._call_api(DRIVER_REVIEW_SETTINGS_BY_MEMBER_V5, "get", {})

    def upload_driver_review_settings(self, **fields):
        """Store the review settings of the authenticated member.

        Sends ``POST /modules/api/v5.0/driver-reviews/settings/upload`` with
        the keywords as the JSON body.

        :param fields: the settings: ``question``, the question the customer
            sees; ``logo_background_color``, e.g. ``"#000000"``; and
            ``logo_picture``, the logo image as a base64 string.
        :return: the decoded JSON reply, or the ``{"errors": ...}`` dict on an
            API error.

        .. versionadded:: 1.0.0
        """
        return self._call_api(DRIVER_REVIEW_SETTINGS_UPLOAD_V5, "post", {}, body=fields)
