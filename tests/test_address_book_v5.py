"""Request-level tests for :class:`route4me.address_book_v5.AddressBookV5`.

Each test pins the HTTP method, URL, query and JSON body one public method
sends. The request guard in ``conftest.py`` checks the host, the endpoint
registry and the bearer token on every request.
"""

import json

import pytest
import responses

from route4me.api_endpoints import (
    ADDRESS_BOOK_CONTACTS_ALL_V5,
    ADDRESS_BOOK_CONTACTS_BATCH_CREATE_V5,
    ADDRESS_BOOK_CONTACTS_BATCH_UPDATE_V5,
    ADDRESS_BOOK_CONTACTS_CLUSTERING_V5,
    ADDRESS_BOOK_CONTACTS_CUSTOM_FIELDS_V5,
    ADDRESS_BOOK_CONTACTS_DELETE_V5,
    ADDRESS_BOOK_CONTACTS_DEPOTS_V5,
    ADDRESS_BOOK_CONTACTS_EXPORT_BY_AREA_IDS_V5,
    ADDRESS_BOOK_CONTACTS_EXPORT_BY_AREAS_V5,
    ADDRESS_BOOK_CONTACTS_EXPORT_V5,
    ADDRESS_BOOK_CONTACTS_PAGINATED_V5,
    ADDRESS_BOOK_CONTACTS_SHOW_V5,
    ADDRESS_BOOK_CONTACTS_UPDATE_BY_AREAS_V5,
    ADDRESS_BOOK_CONTACTS_V5,
    ADDRESS_BOOK_GROUPS_FILTER_ALL_V5,
    ADDRESS_BOOK_GROUPS_V5,
)
from route4me.exceptions import ParamValueException

CONTACT = {"address_1": "1 Example St, Springfield", "cached_lat": 40.1, "cached_lng": -75.2}
AREA_FILTER = {"query": "Example", "bounding_box": {"top": 41, "left": -76, "bottom": 40, "right": -75}}
RULES = {"condition": "AND", "rules": [{"id": "address_1", "field": "address_1", "operator": "contains", "value": "a"}]}

#: (method, args, kwargs, HTTP method, URL, query, JSON body or None).
CASES = [
    (
        "get_address_book_contacts",
        (),
        {"query": "Example", "limit": 10, "offset": 0},
        "GET",
        ADDRESS_BOOK_CONTACTS_ALL_V5,
        {"query": "Example", "limit": "10", "offset": "0"},
        None,
    ),
    (
        "get_address_book_contacts_by_body",
        (),
        {"fields": ["address_id"], "filter": {"display": "routed"}, "limit": 5},
        "POST",
        ADDRESS_BOOK_CONTACTS_ALL_V5,
        {},
        {"fields": ["address_id"], "filter": {"display": "routed"}, "limit": 5},
    ),
    (
        "get_address_book_contacts_paginated",
        (),
        {"display": "unrouted", "page": 2, "per_page": 20},
        "GET",
        ADDRESS_BOOK_CONTACTS_PAGINATED_V5,
        {"display": "unrouted", "page": "2", "per_page": "20"},
        None,
    ),
    (
        "get_address_book_contacts_paginated_by_body",
        (),
        {"order_by": [["address_alias", "asc"]], "page": 1, "per_page": 10},
        "POST",
        ADDRESS_BOOK_CONTACTS_PAGINATED_V5,
        {},
        {"order_by": [["address_alias", "asc"]], "page": 1, "per_page": 10},
    ),
    (
        "get_address_book_contacts_clustering",
        (),
        {"display": "all", "query": "Example"},
        "GET",
        ADDRESS_BOOK_CONTACTS_CLUSTERING_V5,
        {"display": "all", "query": "Example"},
        None,
    ),
    (
        "get_address_book_contacts_clustering_by_body",
        (),
        {"clustering": {"precision": 5}, "filter": {"display": "all"}},
        "POST",
        ADDRESS_BOOK_CONTACTS_CLUSTERING_V5,
        {},
        {"clustering": {"precision": 5}, "filter": {"display": "all"}},
    ),
    (
        "get_address_book_contacts_by_ids",
        (),
        {"address_ids": [1, 2]},
        "POST",
        ADDRESS_BOOK_CONTACTS_SHOW_V5,
        {},
        {"address_ids": [1, 2]},
    ),
    ("get_depots_from_address_book", (), {}, "GET", ADDRESS_BOOK_CONTACTS_DEPOTS_V5, {}, None),
    ("get_custom_fields", (), {}, "GET", ADDRESS_BOOK_CONTACTS_CUSTOM_FIELDS_V5, {}, None),
    ("add_address_book_contact", (), CONTACT, "POST", ADDRESS_BOOK_CONTACTS_V5, {}, CONTACT),
    (
        "batch_create_address_book_contacts",
        (),
        {"data": [CONTACT, CONTACT]},
        "POST",
        ADDRESS_BOOK_CONTACTS_BATCH_CREATE_V5,
        {},
        {"data": [CONTACT, CONTACT]},
    ),
    (
        "update_address_book_contact",
        (7,),
        {**CONTACT, "first_name": "Jane"},
        "PUT",
        f"{ADDRESS_BOOK_CONTACTS_V5}/7",
        {},
        {**CONTACT, "first_name": "Jane"},
    ),
    (
        "batch_update_address_book_contact",
        (),
        {"address_ids": [1, 2], "address_group": "North"},
        "PUT",
        ADDRESS_BOOK_CONTACTS_BATCH_UPDATE_V5,
        {},
        {"address_ids": [1, 2], "address_group": "North"},
    ),
    (
        "update_address_book_contact_by_areas",
        (),
        {"filter": AREA_FILTER, "data": {"address_group": "North"}},
        "PUT",
        ADDRESS_BOOK_CONTACTS_UPDATE_BY_AREAS_V5,
        {},
        {"filter": AREA_FILTER, "data": {"address_group": "North"}},
    ),
    (
        "remove_address_book_contacts",
        (),
        {"address_ids": [1, 2]},
        "DELETE",
        ADDRESS_BOOK_CONTACTS_DELETE_V5,
        {},
        {"address_ids": [1, 2]},
    ),
    (
        "export_addresses",
        (),
        {"ids": [1, 2], "filename": "contacts", "extension": "csv"},
        "POST",
        ADDRESS_BOOK_CONTACTS_EXPORT_V5,
        {},
        {"ids": [1, 2], "filename": "contacts", "extension": "csv"},
    ),
    (
        "export_addresses_by_areas",
        (),
        {"filter": AREA_FILTER},
        "POST",
        ADDRESS_BOOK_CONTACTS_EXPORT_BY_AREAS_V5,
        {},
        {"filter": AREA_FILTER},
    ),
    (
        "export_addresses_by_area_ids",
        (),
        {"territory_ids": ["TERRITORY-1"], "filename": "north"},
        "POST",
        ADDRESS_BOOK_CONTACTS_EXPORT_BY_AREA_IDS_V5,
        {},
        {"territory_ids": ["TERRITORY-1"], "filename": "north"},
    ),
    ("get_address_book_groups", (), {}, "GET", ADDRESS_BOOK_GROUPS_V5, {}, None),
    (
        "filter_contacts_by_group_rules",
        ({"rules": RULES, "limit": 10},),
        {"display": "routed"},
        "POST",
        ADDRESS_BOOK_GROUPS_FILTER_ALL_V5,
        {"display": "routed"},
        {"rules": RULES, "limit": 10},
    ),
]


@pytest.mark.parametrize(
    ("method", "args", "kwargs", "http_method", "url", "query", "body"),
    CASES,
    ids=[case[0] for case in CASES],
)
def test_each_method_sends_its_request(
    client, mocked, last_request, query_of, method, args, kwargs, http_method, url, query, body
):
    mocked.add(http_method, url, json={"status": True}, status=200)

    result = getattr(client.address_book_v5, method)(*args, **kwargs)

    request = last_request()
    assert result == {"status": True}
    assert request.method == http_method
    assert request.url.split("?")[0] == url
    assert query_of(request) == query
    if body is None:
        assert not request.body
    else:
        assert json.loads(request.body) == body


def test_a_query_list_is_sent_with_bracketed_keys(client, mocked, last_request, query_of):
    """PHP keeps only the last of ``display_list=a&display_list=b``."""
    mocked.add(responses.GET, ADDRESS_BOOK_CONTACTS_ALL_V5, json={"results": []}, status=200)

    client.address_book_v5.get_address_book_contacts(display_list=["routed", "unrouted"])

    assert query_of(last_request()) == {"display_list[]": ["routed", "unrouted"]}


def test_query_values_do_not_leak_into_the_next_call(client, mocked, last_request, query_of):
    mocked.add(responses.GET, ADDRESS_BOOK_CONTACTS_ALL_V5, json={"results": []}, status=200)
    client.address_book_v5.get_address_book_contacts(query="Example")

    client.address_book_v5.get_address_book_contacts()

    assert query_of(last_request()) == {}


def test_a_contact_id_with_a_slash_stays_in_its_path_segment(client, mocked, last_request):
    mocked.add(responses.PUT, f"{ADDRESS_BOOK_CONTACTS_V5}/a%2Fb", json={"address_id": 1}, status=200)

    client.address_book_v5.update_address_book_contact("a/b", **CONTACT)

    assert last_request().url == f"{ADDRESS_BOOK_CONTACTS_V5}/a%2Fb"


@pytest.mark.parametrize("address_id", ["", None])
def test_an_empty_contact_id_is_rejected_before_any_request(client, mocked, address_id):
    with pytest.raises(ParamValueException):
        client.address_book_v5.update_address_book_contact(address_id, **CONTACT)

    assert not mocked.calls


@pytest.mark.parametrize(
    ("method", "args", "kwargs", "missing"),
    [
        ("add_address_book_contact", (), {"address_1": "1 Example St"}, "cached_lat, cached_lng"),
        ("update_address_book_contact", (7,), {"cached_lat": 40.1, "cached_lng": -75.2}, "address_1"),
        ("filter_contacts_by_group_rules", ({"limit": 10},), {}, "rules"),
    ],
)
def test_a_missing_required_field_is_named_before_any_request(client, mocked, method, args, kwargs, missing):
    with pytest.raises(ParamValueException) as excinfo:
        getattr(client.address_book_v5, method)(*args, **kwargs)

    assert excinfo.value.param == missing
    assert not mocked.calls


def test_an_api_error_is_returned_as_a_dict(client, mocked):
    mocked.add(
        responses.GET,
        ADDRESS_BOOK_CONTACTS_DEPOTS_V5,
        json={"status": False, "code": 403, "messages": ["Forbidden"]},
        status=403,
    )

    assert client.address_book_v5.get_depots_from_address_book() == {"errors": ["Forbidden"]}


def test_a_queued_job_returns_the_empty_body_and_keeps_the_headers(client, mocked):
    mocked.add(
        responses.POST,
        ADDRESS_BOOK_CONTACTS_EXPORT_V5,
        body=b"",
        status=202,
        headers={"Location": "https://wh.route4me.com/modules/api/v5.0/address-book/job-tracker/status/JOB-1"},
    )

    result = client.address_book_v5.export_addresses(ids=[1])

    assert result == b""
    assert client.address_book_v5.response.status_code == 202
    assert client.address_book_v5.response.headers["Location"].endswith("/job-tracker/status/JOB-1")


def test_a_job_endpoint_returns_a_json_reply_decoded(client, mocked):
    mocked.add(responses.DELETE, ADDRESS_BOOK_CONTACTS_DELETE_V5, json={"status": True}, status=200)

    assert client.address_book_v5.remove_address_book_contacts(address_ids=[1]) == {"status": True}


def test_a_job_endpoint_returns_an_api_error_as_a_dict(client, mocked):
    mocked.add(
        responses.PUT,
        ADDRESS_BOOK_CONTACTS_UPDATE_BY_AREAS_V5,
        json={"status": False, "code": 406, "messages": {"filter": ["The filter is required."]}},
        status=406,
    )

    result = client.address_book_v5.update_address_book_contact_by_areas(data={"address_group": "North"})

    assert result == {"errors": ["The filter is required."]}
