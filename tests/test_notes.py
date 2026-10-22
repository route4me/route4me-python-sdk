"""Request-level tests for :class:`route4me.notes.Notes`.

Each test pins the HTTP method, URL, query string and JSON body the SDK sends
for one public method.
"""

import json

import pytest
import responses

from route4me.api_endpoints import (
    NOTE_CUSTOM_TYPES_V4,
    NOTES_BULK_CREATE_V5,
    NOTES_BY_DESTINATION_V5,
    NOTES_BY_ROUTE_V5,
    NOTES_CUSTOM_TYPES_V5,
    NOTES_V5,
)
from route4me.exceptions import ParamValueException

ROUTE_ID = "C0FFEE00C0FFEE00C0FFEE00C0FFEE00"
NOTE_ID = 7
DESTINATION_ID = 98765
NOTE = {"route_id": ROUTE_ID, "strNoteContents": "Left at the front door"}


def body_of(request):
    """Decode a JSON request body, or ``None`` when there is none."""
    return None if request.body is None else json.loads(request.body)


class TestNotesV5:
    def test_create_note_posts_the_note(self, client, mocked, last_request, query_of):
        mocked.add(responses.POST, NOTES_V5, json={"note_id": NOTE_ID}, status=200)

        result = client.notes.create_note(**NOTE, strUpdateType="dropoff", device_type="web")

        assert result == {"note_id": NOTE_ID}
        assert last_request().method == "POST"
        assert last_request().url.split("?")[0] == NOTES_V5
        assert query_of(last_request()) == {}
        assert body_of(last_request()) == {**NOTE, "strUpdateType": "dropoff", "device_type": "web"}

    @pytest.mark.parametrize("field", ["route_id", "strNoteContents"])
    def test_create_note_requires_the_route_and_the_text(self, client, mocked, field):
        fields = {name: value for name, value in NOTE.items() if name != field}

        with pytest.raises(ParamValueException) as error:
            client.notes.create_note(**fields)

        assert error.value.param == field
        assert not mocked.calls

    def test_bulk_create_notes_posts_the_list(self, client, mocked, last_request, query_of):
        mocked.add(responses.POST, NOTES_BULK_CREATE_V5, json={"status": True, "async": True}, status=200)

        result = client.notes.bulk_create_notes(notes=[NOTE, NOTE], device_type="web")

        assert result == {"status": True, "async": True}
        assert last_request().method == "POST"
        assert last_request().url.split("?")[0] == NOTES_BULK_CREATE_V5
        assert query_of(last_request()) == {}
        assert body_of(last_request()) == {"notes": [NOTE, NOTE], "device_type": "web"}

    @pytest.mark.parametrize(
        ("fields", "param"),
        [
            ({}, "notes"),
            ({"notes": []}, "notes"),
            ({"notes": [NOTE, {"route_id": ROUTE_ID}]}, "notes[1]"),
        ],
    )
    def test_bulk_create_notes_checks_every_note(self, client, mocked, fields, param):
        with pytest.raises(ParamValueException) as error:
            client.notes.bulk_create_notes(**fields)

        assert error.value.param == param
        assert not mocked.calls

    @pytest.mark.parametrize(
        ("method", "verb"),
        [("get_note", responses.GET), ("delete_note", responses.DELETE)],
    )
    def test_get_and_delete_put_the_note_id_in_the_path(self, client, mocked, last_request, query_of, method, verb):
        mocked.add(verb, f"{NOTES_V5}/{NOTE_ID}", json={"note_id": NOTE_ID}, status=200)

        assert getattr(client.notes, method)(NOTE_ID) == {"note_id": NOTE_ID}
        assert last_request().method == verb
        assert last_request().url.split("?")[0] == f"{NOTES_V5}/{NOTE_ID}"
        assert query_of(last_request()) == {}
        assert body_of(last_request()) is None

    def test_update_note_posts_the_changes(self, client, mocked, last_request, query_of):
        mocked.add(responses.POST, f"{NOTES_V5}/{NOTE_ID}", json={"note_id": NOTE_ID}, status=200)

        client.notes.update_note(NOTE_ID, strNoteContents="Signed by the customer", strUpdateType="dropoff")

        assert last_request().method == "POST"
        assert last_request().url.split("?")[0] == f"{NOTES_V5}/{NOTE_ID}"
        assert query_of(last_request()) == {}
        assert body_of(last_request()) == {"strNoteContents": "Signed by the customer", "strUpdateType": "dropoff"}

    @pytest.mark.parametrize(
        ("method", "base", "path_id"),
        [
            ("get_notes_by_route", NOTES_BY_ROUTE_V5, ROUTE_ID),
            ("get_notes_by_destination", NOTES_BY_DESTINATION_V5, DESTINATION_ID),
        ],
    )
    def test_listings_send_the_page_in_the_query(self, client, mocked, last_request, query_of, method, base, path_id):
        mocked.add(responses.GET, f"{base}/{path_id}", json={"data": []}, status=200)

        assert getattr(client.notes, method)(path_id, page=2, per_page=50) == {"data": []}
        assert last_request().method == "GET"
        assert last_request().url.split("?")[0] == f"{base}/{path_id}"
        assert query_of(last_request()) == {"page": "2", "per_page": "50"}

    def test_listings_leave_out_the_page_when_not_given(self, client, mocked, last_request, query_of):
        mocked.add(responses.GET, f"{NOTES_BY_ROUTE_V5}/{ROUTE_ID}", json={"data": []}, status=200)

        client.notes.get_notes_by_route(ROUTE_ID)

        assert query_of(last_request()) == {}

    def test_get_note_custom_types(self, client, mocked, last_request, query_of):
        mocked.add(responses.GET, NOTES_CUSTOM_TYPES_V5, json={"data": []}, status=200)

        assert client.notes.get_note_custom_types() == {"data": []}
        assert last_request().method == "GET"
        assert query_of(last_request()) == {}

    def test_create_note_custom_type_posts_the_type(self, client, mocked, last_request, query_of):
        mocked.add(responses.POST, NOTES_CUSTOM_TYPES_V5, json={"data": []}, status=200)

        client.notes.create_note_custom_type(
            note_custom_type="Gate code", note_custom_type_values=["A", "B"], note_custom_field_type=1
        )

        assert last_request().method == "POST"
        assert last_request().url.split("?")[0] == NOTES_CUSTOM_TYPES_V5
        assert query_of(last_request()) == {}
        assert body_of(last_request()) == {
            "note_custom_type": "Gate code",
            "note_custom_type_values": ["A", "B"],
            "note_custom_field_type": 1,
        }

    def test_create_note_custom_type_requires_the_values(self, client, mocked):
        with pytest.raises(ParamValueException) as error:
            client.notes.create_note_custom_type(note_custom_type="Gate code")

        assert error.value.param == "note_custom_type_values"
        assert not mocked.calls

    def test_a_note_id_with_a_slash_stays_one_path_segment(self, client, mocked, last_request):
        mocked.add(responses.GET, f"{NOTES_V5}/a%2Fb", json={}, status=200)

        client.notes.get_note("a/b")

        assert last_request().path_url == "/modules/api/v5.0/notes/a%2Fb"

    @pytest.mark.parametrize(
        "call",
        [
            lambda notes: notes.get_note(""),
            lambda notes: notes.update_note("", strNoteContents="x"),
            lambda notes: notes.delete_note(None),
            lambda notes: notes.get_notes_by_route(" "),
            lambda notes: notes.get_notes_by_destination(""),
        ],
    )
    def test_an_empty_id_is_rejected_before_any_request(self, client, mocked, call):
        with pytest.raises(ParamValueException):
            call(client.notes)

        assert not mocked.calls

    def test_an_api_error_is_returned_as_a_dict(self, client, mocked):
        mocked.add(
            responses.GET,
            f"{NOTES_V5}/{NOTE_ID}",
            json={"status": False, "code": 404, "messages": ["Note not found"]},
            status=404,
        )

        assert client.notes.get_note(NOTE_ID) == {"errors": ["Note not found"]}


class TestCustomNoteTypesV4:
    def test_add_custom_note_type_posts_the_type(self, client, mocked, last_request, query_of, api_key):
        mocked.add(responses.POST, NOTE_CUSTOM_TYPES_V4, json={"result": "OK", "affected": 1}, status=200)

        result = client.notes.add_custom_note_type(note_custom_type="Language", note_custom_type_values=["EN", "FR"])

        assert result == {"result": "OK", "affected": 1}
        assert last_request().method == "POST"
        assert last_request().url.split("?")[0] == NOTE_CUSTOM_TYPES_V4
        assert query_of(last_request()) == {"api_key": api_key}
        assert body_of(last_request()) == {"note_custom_type": "Language", "note_custom_type_values": ["EN", "FR"]}

    def test_add_custom_note_type_requires_the_name(self, client, mocked):
        with pytest.raises(ParamValueException) as error:
            client.notes.add_custom_note_type(note_custom_type_values=["EN"])

        assert error.value.param == "note_custom_type"
        assert not mocked.calls

    def test_get_all_custom_note_types(self, client, mocked, last_request, query_of, api_key):
        mocked.add(responses.GET, NOTE_CUSTOM_TYPES_V4, json=[{"note_custom_type_id": 3}], status=200)

        assert client.notes.get_all_custom_note_types() == [{"note_custom_type_id": 3}]
        assert last_request().method == "GET"
        assert query_of(last_request()) == {"api_key": api_key}
        assert body_of(last_request()) is None

    def test_remove_custom_note_type_sends_the_id_in_the_body(self, client, mocked, last_request, query_of, api_key):
        mocked.add(responses.DELETE, NOTE_CUSTOM_TYPES_V4, json={"result": "OK", "affected": 1}, status=200)

        client.notes.remove_custom_note_type(3)

        assert last_request().method == "DELETE"
        assert last_request().url.split("?")[0] == NOTE_CUSTOM_TYPES_V4
        assert query_of(last_request()) == {"api_key": api_key}
        assert body_of(last_request()) == {"id": 3}

    @pytest.mark.parametrize("value", [None, "", "  "])
    def test_remove_custom_note_type_requires_the_id(self, client, mocked, value):
        with pytest.raises(ParamValueException):
            client.notes.remove_custom_note_type(value)

        assert not mocked.calls

    def test_an_api_error_is_returned_as_a_dict(self, client, mocked):
        mocked.add(responses.GET, NOTE_CUSTOM_TYPES_V4, json={"errors": ["Authentication failed"]}, status=401)

        assert client.notes.get_all_custom_note_types() == {"errors": ["Authentication failed"]}
