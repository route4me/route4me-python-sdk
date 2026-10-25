"""Request-level tests for the group and search methods of :class:`route4me.address_book.AddressBook`.

The contact methods are covered in ``test_crud_resources.py``.
"""

import json

import pytest
import responses

from route4me.api_endpoints import (
    ADDRESS_BOOK_GROUP,
    ADDRESS_BOOK_GROUP_SEARCH,
    ADDRESSBOOK,
    SAVE_GEOCODED_ADDRESSES,
)
from route4me.exceptions import ParamValueException

GROUP_ID = "GROUP-1"
GROUP_FILTER = {"condition": "AND", "rules": [{"id": "address_1", "field": "address_1", "operator": "contains"}]}

#: (method, args, kwargs, HTTP method, URL, query without api_key, JSON body or None).
CASES = [
    (
        "search_address_book_contacts_by_filter",
        ({"fields": ["address_id"], "filter": {"query": "Example", "display": "all"}},),
        {"offset": 0, "limit": 10},
        "POST",
        ADDRESSBOOK,
        {"offset": "0", "limit": "10"},
        {"fields": ["address_id"], "filter": {"query": "Example", "display": "all"}},
    ),
    (
        "get_address_book_contacts_by_group",
        ({"fields": ["address_id"]},),
        {"group_id": GROUP_ID},
        "POST",
        ADDRESS_BOOK_GROUP_SEARCH,
        {"group_id": GROUP_ID},
        {"fields": ["address_id"]},
    ),
    (
        "save_geocoded_addresses_to_database",
        (),
        {"optimization_problem_id": "OPTIMIZATION-1"},
        "POST",
        SAVE_GEOCODED_ADDRESSES,
        {},
        {"optimization_problem_id": "OPTIMIZATION-1"},
    ),
    (
        "add_address_book_group",
        (),
        {"group_name": "North", "group_color": "92e1c0", "filter": GROUP_FILTER},
        "POST",
        ADDRESS_BOOK_GROUP,
        {},
        {"group_name": "North", "group_color": "92e1c0", "filter": GROUP_FILTER},
    ),
    (
        "get_address_book_groups",
        (),
        {"offset": 0, "limit": 5},
        "GET",
        ADDRESS_BOOK_GROUP,
        {"offset": "0", "limit": "5"},
        None,
    ),
    ("get_address_book_groups", (), {"group_id": GROUP_ID}, "GET", ADDRESS_BOOK_GROUP, {"group_id": GROUP_ID}, None),
    (
        "update_address_book_group",
        (),
        {"group_id": GROUP_ID, "group_color": "cd74e6"},
        "PUT",
        ADDRESS_BOOK_GROUP,
        {},
        {"group_id": GROUP_ID, "group_color": "cd74e6"},
    ),
    (
        "remove_address_book_group",
        (),
        {"group_id": GROUP_ID},
        "DELETE",
        ADDRESS_BOOK_GROUP,
        {},
        {"group_id": GROUP_ID},
    ),
]


@pytest.mark.parametrize(
    ("method", "args", "kwargs", "http_method", "url", "query", "body"),
    CASES,
    ids=[f"{case[0]}-{i}" for i, case in enumerate(CASES)],
)
def test_each_method_sends_its_request(
    client, mocked, last_request, query_of, api_key, method, args, kwargs, http_method, url, query, body
):
    mocked.add(http_method, url, json={"status": True}, status=200)

    result = getattr(client.address_book, method)(*args, **kwargs)

    request = last_request()
    assert result == {"status": True}
    assert request.method == http_method
    assert request.url.split("?")[0] == url
    assert query_of(request) == {"api_key": api_key, **query}
    if body is None:
        assert not request.body
    else:
        assert json.loads(request.body) == body


def test_contacts_by_group_sends_an_empty_body_without_fields(client, mocked, last_request):
    mocked.add(responses.POST, ADDRESS_BOOK_GROUP_SEARCH, json={"results": []}, status=200)

    client.address_book.get_address_book_contacts_by_group(group_id=GROUP_ID)

    assert json.loads(last_request().body) == {}


def test_a_group_id_with_a_slash_is_encoded(client, mocked, last_request):
    mocked.add(responses.GET, ADDRESS_BOOK_GROUP, json={"group_id": GROUP_ID}, status=200)

    client.address_book.get_address_book_groups(group_id="a/b")

    assert "group_id=a%2Fb" in last_request().url


@pytest.mark.parametrize(
    ("method", "args", "kwargs", "missing"),
    [
        ("get_address_book_contacts_by_group", ({"fields": ["address_id"]},), {}, "group_id"),
        ("save_geocoded_addresses_to_database", (), {}, "optimization_problem_id"),
        ("update_address_book_group", (), {"group_color": "cd74e6"}, "group_id"),
        ("remove_address_book_group", (), {}, "group_id"),
    ],
)
def test_a_missing_id_is_rejected_before_any_request(client, mocked, method, args, kwargs, missing):
    with pytest.raises(ParamValueException) as excinfo:
        getattr(client.address_book, method)(*args, **kwargs)

    assert excinfo.value.param == missing
    assert not mocked.calls


def test_an_api_error_is_returned_as_a_dict(client, mocked):
    mocked.add(responses.GET, ADDRESS_BOOK_GROUP, json={"errors": ["Group not found"]}, status=404)

    assert client.address_book.get_address_book_groups(group_id=GROUP_ID) == {"errors": ["Group not found"]}
