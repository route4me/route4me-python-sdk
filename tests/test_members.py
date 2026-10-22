"""Request-level tests for the V4 user methods of :class:`route4me.members.Members`.

The older :class:`~route4me.members.Members` methods are tested in
``test_members_gps.py``.
"""

import json

import responses

from route4me.api_endpoints import MEMBER_CAPABILITIES, USER_URL

MEMBER_ID = 4321


class TestMembersUsers:
    def test_create_user_posts_the_user_as_json(self, client, mocked, last_request, query_of):
        mocked.add(responses.POST, USER_URL, json={"member_id": MEMBER_ID}, status=200)
        user = {
            "member_first_name": "Ada",
            "member_last_name": "Lovelace",
            "member_email": "ada@example.com",
            "member_type": "SUB_ACCOUNT_DRIVER",
            "OWNER_MEMBER_ID": 1234,
        }

        assert client.members.create_user(**user) == {"member_id": MEMBER_ID}
        assert last_request().method == "POST"
        assert query_of(last_request()) == {"api_key": client.key}
        assert json.loads(last_request().body) == user

    def test_user_update_sends_the_member_id_in_the_query(self, client, mocked, last_request, query_of):
        mocked.add(responses.PUT, USER_URL, json={"member_id": MEMBER_ID}, status=200)

        client.members.user_update(MEMBER_ID, member_phone="555-0100")

        assert last_request().method == "PUT"
        assert query_of(last_request()) == {"api_key": client.key, "member_id": str(MEMBER_ID)}
        assert json.loads(last_request().body) == {"member_phone": "555-0100"}

    def test_user_delete_sends_the_member_id_in_the_query(self, client, mocked, last_request, query_of):
        mocked.add(responses.DELETE, USER_URL, json={"status": True}, status=200)

        assert client.members.user_delete(MEMBER_ID) == {"status": True}
        assert last_request().method == "DELETE"
        assert query_of(last_request()) == {"api_key": client.key, "member_id": str(MEMBER_ID)}
        assert not last_request().body

    def test_get_member_capabilities(self, client, mocked, last_request, query_of):
        mocked.add(responses.GET, MEMBER_CAPABILITIES, json={"commercial": True}, status=200)

        assert client.members.get_member_capabilities() == {"commercial": True}
        assert last_request().method == "GET"
        assert query_of(last_request()) == {"api_key": client.key}

    def test_an_api_error_is_returned_as_a_dict(self, client, mocked, load_fixture):
        mocked.add(responses.PUT, USER_URL, json=load_fixture("error_v4"), status=401)

        assert client.members.user_update(MEMBER_ID, member_phone="555-0100") == {"errors": ["The API key is invalid."]}
