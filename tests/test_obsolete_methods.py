"""The methods whose operation the C# SDK marks ``[Obsolete]`` warn and name their replacement.

They still send the same request as before; only the warning is new.
"""

import re

import pytest
import responses

ANY_V4 = re.compile(r"https://api\.route4me\.com/.*")
ROUTE_ID = "C0FFEE00C0FFEE00C0FFEE00C0FFEE00"

CASES = [
    ("members", "get_api_key_users", (), {}, "TeamV5.get_team_members"),
    ("members", "create_user", (), {"member_email": "driver@example.com"}, "TeamV5.create_team_member"),
    ("members", "user_update", (1002,), {"member_first_name": "Ann"}, "TeamV5.update_team_member"),
    ("members", "user_delete", (1002,), {}, "TeamV5.remove_team_member"),
    ("address_book", "get_addressbook_contacts", (), {}, "AddressBookV5.get_address_book_contacts"),
    (
        "address_book",
        "create_contact",
        (),
        {"address_1": "1 Example St", "cached_lat": 40.1, "cached_lng": -75.2},
        "AddressBookV5.add_address_book_contact",
    ),
    (
        "address_book",
        "update_contact",
        (),
        {"address_id": 7, "address_1": "2 Example St"},
        "AddressBookV5.update_address_book_contact",
    ),
    (
        "address_book",
        "delete_addressbook_contact",
        (),
        {"address_ids": [7]},
        "AddressBookV5.remove_address_book_contacts",
    ),
    (
        "route",
        "resequence_route_all",
        (),
        {"route_id": ROUTE_ID, "disable_optimization": 0, "optimize": "Distance"},
        "Route.update_route with reoptimize=1",
    ),
]


@pytest.mark.parametrize(("resource", "method", "args", "kwargs", "replacement"), CASES, ids=[c[1] for c in CASES])
def test_an_obsolete_operation_warns_and_still_sends_its_request(
    client, mocked, resource, method, args, kwargs, replacement
):
    for verb in (responses.GET, responses.POST, responses.PUT, responses.DELETE):
        mocked.add(verb, ANY_V4, json={}, status=200)

    with pytest.warns(DeprecationWarning, match=re.escape(f"Use {replacement}.")):
        getattr(getattr(client, resource), method)(*args, **kwargs)

    assert len(mocked.calls) == 1
