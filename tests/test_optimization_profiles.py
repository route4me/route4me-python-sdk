"""Request-level tests for the optimization profile CRUD and entity methods.

The list method, :meth:`OptimizationProfiles.get_optimization_profiles
<route4me.optimization_profiles.OptimizationProfiles.get_optimization_profiles>`,
is covered in ``test_v5_resources.py``.
"""

import json
from urllib.parse import urlsplit

import pytest
import responses

from route4me.api_endpoints import (
    OPTIMIZATION_PROFILES_BASE_V5,
    OPTIMIZATION_PROFILES_DELETE_ENTITIES_V5,
    OPTIMIZATION_PROFILES_SAVE_ENTITIES_V5,
)
from route4me.exceptions import ParamValueException

PROFILE_ID = "PROFILE-1"
PROFILE_URL = f"{OPTIMIZATION_PROFILES_BASE_V5}/{PROFILE_ID}"


def path_of(url):
    return urlsplit(url).path


class TestOptimizationProfileCrud:
    def test_create_optimization_profile_posts_the_keywords(self, client, mocked, last_request, query_of):
        body = {"profile_name": "Test profile", "optimization_type": "multi", "avoid_tolls": True}
        mocked.add(responses.POST, OPTIMIZATION_PROFILES_BASE_V5, json={"data": {"id": PROFILE_ID}}, status=200)

        assert client.optimization_profiles.create_optimization_profile(**body) == {"data": {"id": PROFILE_ID}}
        request = last_request()
        assert request.method == "POST"
        assert path_of(request.url) == path_of(OPTIMIZATION_PROFILES_BASE_V5)
        assert query_of(request) == {}
        assert json.loads(request.body) == body

    @pytest.mark.parametrize(
        ("method", "args"),
        [("create_optimization_profile", ()), ("update_optimization_profile", (PROFILE_ID,))],
    )
    def test_a_profile_name_is_required(self, client, mocked, method, args):
        with pytest.raises(ParamValueException) as excinfo:
            getattr(client.optimization_profiles, method)(*args, is_default=False)

        assert excinfo.value.param == "profile_name"
        assert not mocked.calls

    @pytest.mark.parametrize(
        ("method", "http_method"),
        [("get_optimization_profile_by_id", "GET"), ("delete_optimization_profile", "DELETE")],
    )
    def test_puts_the_profile_id_in_the_path(self, client, mocked, last_request, query_of, method, http_method):
        mocked.add(http_method, PROFILE_URL, json={"status": True}, status=200)

        assert getattr(client.optimization_profiles, method)(PROFILE_ID) == {"status": True}
        request = last_request()
        assert request.method == http_method
        assert path_of(request.url) == path_of(PROFILE_URL)
        assert query_of(request) == {}
        assert request.body is None

    def test_update_optimization_profile_puts_the_keywords(self, client, mocked, last_request, query_of):
        mocked.add(responses.PUT, PROFILE_URL, json={"data": {"id": PROFILE_ID}}, status=200)

        client.optimization_profiles.update_optimization_profile(PROFILE_ID, profile_name="Renamed", is_default=True)

        request = last_request()
        assert request.method == "PUT"
        assert path_of(request.url) == path_of(PROFILE_URL)
        assert query_of(request) == {}
        assert json.loads(request.body) == {"profile_name": "Renamed", "is_default": True}

    def test_an_id_cannot_escape_its_path_segment(self, client, monkeypatch):
        urls = []

        def capture(url, params, request_method, **kwargs):
            urls.append(url)
            raise RuntimeError("stop before sending")

        monkeypatch.setattr(client, "_make_request", capture)

        with pytest.raises(RuntimeError):
            client.optimization_profiles.get_optimization_profile_by_id("a/b")

        assert urls == [f"{OPTIMIZATION_PROFILES_BASE_V5}/a%2Fb"]

    @pytest.mark.parametrize(
        ("method", "kwargs"),
        [
            ("get_optimization_profile_by_id", {}),
            ("update_optimization_profile", {"profile_name": "Renamed"}),
            ("delete_optimization_profile", {}),
        ],
    )
    def test_an_empty_id_is_rejected_before_any_request(self, client, mocked, method, kwargs):
        with pytest.raises(ParamValueException):
            getattr(client.optimization_profiles, method)(" ", **kwargs)

        assert not mocked.calls

    def test_an_api_error_is_returned_as_a_dict(self, client, mocked):
        mocked.add(
            responses.DELETE,
            PROFILE_URL,
            json={"status": False, "code": 404, "messages": {"id": ["Optimization profile not found."]}},
            status=404,
        )

        assert client.optimization_profiles.delete_optimization_profile(PROFILE_ID) == {
            "errors": ["Optimization profile not found."]
        }


class TestOptimizationProfileEntities:
    @pytest.mark.parametrize(
        ("method", "url", "items"),
        [
            (
                "save_entities",
                OPTIMIZATION_PROFILES_SAVE_ENTITIES_V5,
                [{"id": PROFILE_ID, "guid": "ENTITY-1", "parts": [{"guid": "PART-1", "data": {}, "config": {}}]}],
            ),
            ("delete_entities", OPTIMIZATION_PROFILES_DELETE_ENTITIES_V5, [{"id": PROFILE_ID}]),
        ],
    )
    def test_posts_the_items(self, client, mocked, last_request, query_of, method, url, items):
        mocked.add(responses.POST, url, json={"items": items}, status=200)

        assert getattr(client.optimization_profiles, method)(items=items) == {"items": items}
        request = last_request()
        assert request.method == "POST"
        assert path_of(request.url) == path_of(url)
        assert query_of(request) == {}
        assert json.loads(request.body) == {"items": items}

    def test_an_api_error_is_returned_as_a_dict(self, client, mocked):
        mocked.add(
            responses.POST,
            OPTIMIZATION_PROFILES_SAVE_ENTITIES_V5,
            json={"status": False, "code": 406, "messages": {"items": ["The items field is required."]}},
            status=406,
        )

        assert client.optimization_profiles.save_entities(items=[]) == {"errors": ["The items field is required."]}
