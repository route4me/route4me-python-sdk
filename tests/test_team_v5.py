"""Request-level tests for :class:`route4me.team_v5.TeamV5`."""

import json

import pytest
import responses

from route4me.api_endpoints import TEAM_BULK_INSERT_V5, TEAM_USERS_V5
from route4me.exceptions import ParamValueException

USER_ID = 4321
MEMBER = {
    "member_first_name": "Ada",
    "member_last_name": "Lovelace",
    "member_email": "ada@example.com",
    "member_type": "SUB_ACCOUNT_DRIVER",
    "OWNER_MEMBER_ID": 1234,
}


class TestTeamV5:
    def test_get_team_members_sends_the_filters_in_the_query(self, client, mocked, last_request, query_of):
        mocked.add(responses.GET, TEAM_USERS_V5, json=[{"member_id": USER_ID}], status=200)

        result = client.team_v5.get_team_members(query="ada", drivers_only=1, facility_ids=["FACILITY-1", "FACILITY-2"])

        assert result == [{"member_id": USER_ID}]
        request = last_request()
        assert request.method == "GET"
        assert request.url.split("?")[0] == TEAM_USERS_V5
        assert query_of(request) == {
            "query": "ada",
            "drivers_only": "1",
            "facility_ids[]": ["FACILITY-1", "FACILITY-2"],
        }
        assert request.body is None

    def test_get_team_members_without_filters_sends_no_query(self, client, mocked, last_request, query_of):
        mocked.add(responses.GET, TEAM_USERS_V5, json=[], status=200)

        assert client.team_v5.get_team_members() == []
        assert query_of(last_request()) == {}

    def test_get_team_member_by_id_puts_the_id_in_the_path(self, client, mocked, last_request, query_of):
        mocked.add(responses.GET, f"{TEAM_USERS_V5}/{USER_ID}", json={"member_id": USER_ID}, status=200)

        assert client.team_v5.get_team_member_by_id(USER_ID) == {"member_id": USER_ID}
        assert last_request().method == "GET"
        assert query_of(last_request()) == {}

    def test_create_team_member_posts_the_member(self, client, mocked, last_request, query_of):
        mocked.add(responses.POST, TEAM_USERS_V5, json={"member_id": USER_ID}, status=200)

        result = client.team_v5.create_team_member(**MEMBER, member_phone="555-0100")

        assert result == {"member_id": USER_ID}
        assert last_request().method == "POST"
        assert query_of(last_request()) == {}
        assert json.loads(last_request().body) == {**MEMBER, "member_phone": "555-0100"}

    @pytest.mark.parametrize("missing", sorted(MEMBER))
    def test_create_team_member_requires_the_spec_fields(self, client, mocked, missing):
        member = {k: v for k, v in MEMBER.items() if k != missing}

        with pytest.raises(ParamValueException) as excinfo:
            client.team_v5.create_team_member(**member)

        assert excinfo.value.param == missing
        assert not mocked.calls

    def test_bulk_create_team_members_posts_the_users_and_the_conflict_rule(self, client, mocked, last_request):
        mocked.add(responses.POST, TEAM_BULK_INSERT_V5, json={}, status=200)

        assert client.team_v5.bulk_create_team_members(users=[MEMBER], conflicts="skip") == {}
        assert last_request().method == "POST"
        assert last_request().url == TEAM_BULK_INSERT_V5
        assert json.loads(last_request().body) == {"users": [MEMBER], "conflicts": "skip"}

    @pytest.mark.parametrize("kwargs", [{}, {"users": []}, {"conflicts": "fail"}])
    def test_bulk_create_team_members_requires_users(self, client, mocked, kwargs):
        with pytest.raises(ParamValueException) as excinfo:
            client.team_v5.bulk_create_team_members(**kwargs)

        assert excinfo.value.param == "users"
        assert not mocked.calls

    def test_update_team_member_patches_the_fields(self, client, mocked, last_request, query_of):
        mocked.add(responses.PATCH, f"{TEAM_USERS_V5}/{USER_ID}", json={"member_id": USER_ID}, status=200)

        skills = {"driver_skills": "Forklift,Hazmat"}
        result = client.team_v5.update_team_member(USER_ID, member_email="ada@example.com", custom_data=skills)

        assert result == {"member_id": USER_ID}
        assert last_request().method == "PATCH"
        assert query_of(last_request()) == {}
        assert json.loads(last_request().body) == {"member_email": "ada@example.com", "custom_data": skills}

    def test_update_team_member_requires_member_email(self, client, mocked):
        with pytest.raises(ParamValueException) as excinfo:
            client.team_v5.update_team_member(USER_ID, member_phone="555-0100")

        assert excinfo.value.param == "member_email"
        assert not mocked.calls

    def test_remove_team_member_sends_a_delete(self, client, mocked, last_request):
        mocked.add(responses.DELETE, f"{TEAM_USERS_V5}/{USER_ID}", json={"member_id": USER_ID}, status=200)

        assert client.team_v5.remove_team_member(USER_ID) == {"member_id": USER_ID}
        assert last_request().method == "DELETE"
        assert not last_request().body

    @pytest.mark.parametrize(
        ("method", "kwargs"),
        [
            ("get_team_member_by_id", {}),
            ("update_team_member", {"member_email": "ada@example.com"}),
            ("remove_team_member", {}),
        ],
    )
    def test_a_user_id_cannot_escape_its_path_segment(self, client, monkeypatch, method, kwargs):
        urls = []

        def capture(url, params, request_method, **_):
            urls.append(url)
            raise RuntimeError("stop before sending")

        monkeypatch.setattr(client, "_make_request", capture)

        with pytest.raises(RuntimeError):
            getattr(client.team_v5, method)("a/b", **kwargs)

        assert urls == [f"{TEAM_USERS_V5}/a%2Fb"]

    @pytest.mark.parametrize(
        ("method", "kwargs"),
        [
            ("get_team_member_by_id", {}),
            ("update_team_member", {"member_email": "ada@example.com"}),
            ("remove_team_member", {}),
        ],
    )
    def test_an_empty_user_id_is_rejected_before_any_request(self, client, mocked, method, kwargs):
        with pytest.raises(ParamValueException):
            getattr(client.team_v5, method)("", **kwargs)

        assert not mocked.calls

    def test_an_api_error_is_returned_as_a_dict(self, client, mocked):
        error = {"status": False, "code": 404, "exit_code": 1, "messages": ["Member not found"]}
        mocked.add(responses.GET, f"{TEAM_USERS_V5}/{USER_ID}", json=error, status=404)

        assert client.team_v5.get_team_member_by_id(USER_ID) == {"errors": ["Member not found"]}
