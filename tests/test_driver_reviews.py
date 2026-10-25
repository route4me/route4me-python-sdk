"""Request-level tests for :class:`route4me.driver_reviews.DriverReviews`.

Each test pins the HTTP method, URL, query string and JSON body the SDK sends
for one public method.
"""

import json

import pytest
import responses

from route4me.api_endpoints import (
    DRIVER_REVIEW_SETTINGS_BY_MEMBER_V5,
    DRIVER_REVIEW_SETTINGS_UPLOAD_V5,
    DRIVER_REVIEWS_V5,
)
from route4me.exceptions import ParamValueException

RATING_ID = "REVIEW-1"
REVIEW = {"tracking_number": "TRACK-1", "rating": 5, "review": "On time and friendly"}


def body_of(request):
    """Decode a JSON request body, or ``None`` when there is none."""
    return None if request.body is None else json.loads(request.body)


class TestDriverReviews:
    def test_get_driver_review_list_sends_the_filters(self, client, mocked, last_request, query_of):
        mocked.add(responses.GET, DRIVER_REVIEWS_V5, json={"data": []}, status=200)

        result = client.driver_reviews.get_driver_review_list(
            rating=5, member_id=42, start="2026-10-01", end="2026-10-31", page=2, per_page=20
        )

        assert result == {"data": []}
        assert last_request().method == "GET"
        assert last_request().url.split("?")[0] == DRIVER_REVIEWS_V5
        assert query_of(last_request()) == {
            "rating": "5",
            "member_id": "42",
            "start": "2026-10-01",
            "end": "2026-10-31",
            "page": "2",
            "per_page": "20",
        }
        assert body_of(last_request()) is None

    def test_get_driver_review_list_without_filters_sends_no_query(self, client, mocked, last_request, query_of):
        mocked.add(responses.GET, DRIVER_REVIEWS_V5, json={"data": []}, status=200)

        client.driver_reviews.get_driver_review_list()

        assert query_of(last_request()) == {}

    def test_get_driver_review_by_id_puts_the_id_in_the_path(self, client, mocked, last_request, query_of):
        mocked.add(responses.GET, f"{DRIVER_REVIEWS_V5}/{RATING_ID}", json={"data": REVIEW}, status=200)

        assert client.driver_reviews.get_driver_review_by_id(RATING_ID) == {"data": REVIEW}
        assert last_request().method == "GET"
        assert last_request().url.split("?")[0] == f"{DRIVER_REVIEWS_V5}/{RATING_ID}"
        assert query_of(last_request()) == {}

    def test_create_driver_review_posts_the_review(self, client, mocked, last_request, query_of):
        mocked.add(responses.POST, DRIVER_REVIEWS_V5, json={"data": REVIEW}, status=200)

        client.driver_reviews.create_driver_review(**REVIEW)

        assert last_request().method == "POST"
        assert last_request().url.split("?")[0] == DRIVER_REVIEWS_V5
        assert query_of(last_request()) == {}
        assert body_of(last_request()) == REVIEW

    @pytest.mark.parametrize(("method", "verb"), [("update_driver_review", "PATCH"), ("replace_driver_review", "PUT")])
    def test_updates_send_the_review_to_its_url(self, client, mocked, last_request, query_of, method, verb):
        mocked.add(verb, f"{DRIVER_REVIEWS_V5}/{RATING_ID}", json={"data": REVIEW}, status=200)

        getattr(client.driver_reviews, method)(RATING_ID, review="Updated review", rating=4)

        assert last_request().method == verb
        assert last_request().url.split("?")[0] == f"{DRIVER_REVIEWS_V5}/{RATING_ID}"
        assert query_of(last_request()) == {}
        assert body_of(last_request()) == {"review": "Updated review", "rating": 4}

    def test_get_driver_review_settings_by_member(self, client, mocked, last_request, query_of):
        mocked.add(responses.GET, DRIVER_REVIEW_SETTINGS_BY_MEMBER_V5, json={"data": {"question": "?"}}, status=200)

        assert client.driver_reviews.get_driver_review_settings_by_member() == {"data": {"question": "?"}}
        assert last_request().method == "GET"
        assert last_request().url.split("?")[0] == DRIVER_REVIEW_SETTINGS_BY_MEMBER_V5
        assert query_of(last_request()) == {}

    def test_upload_driver_review_settings_posts_the_settings(self, client, mocked, last_request, query_of):
        mocked.add(responses.POST, DRIVER_REVIEW_SETTINGS_UPLOAD_V5, json={"data": {}}, status=200)

        client.driver_reviews.upload_driver_review_settings(
            question="How was your delivery?", logo_background_color="#000000", logo_picture="iVBORw0KGgo="
        )

        assert last_request().method == "POST"
        assert last_request().url.split("?")[0] == DRIVER_REVIEW_SETTINGS_UPLOAD_V5
        assert query_of(last_request()) == {}
        assert body_of(last_request()) == {
            "question": "How was your delivery?",
            "logo_background_color": "#000000",
            "logo_picture": "iVBORw0KGgo=",
        }

    def test_a_rating_id_with_a_slash_stays_one_path_segment(self, client, mocked, last_request):
        mocked.add(responses.GET, f"{DRIVER_REVIEWS_V5}/a%2Fb", json={}, status=200)

        client.driver_reviews.get_driver_review_by_id("a/b")

        assert last_request().path_url == "/modules/api/v5.0/driver-reviews/a%2Fb"

    @pytest.mark.parametrize("method", ["get_driver_review_by_id", "update_driver_review", "replace_driver_review"])
    def test_an_empty_rating_id_is_rejected_before_any_request(self, client, mocked, method):
        with pytest.raises(ParamValueException):
            getattr(client.driver_reviews, method)("")

        assert not mocked.calls

    def test_an_api_error_is_returned_as_a_dict(self, client, mocked):
        mocked.add(
            responses.POST,
            DRIVER_REVIEWS_V5,
            json={"status": False, "code": 406, "messages": {"rating": ["The rating must not be greater than 5."]}},
            status=406,
        )

        result = client.driver_reviews.create_driver_review(tracking_number="TRACK-1", rating=6)

        assert result == {"errors": ["The rating must not be greater than 5."]}
