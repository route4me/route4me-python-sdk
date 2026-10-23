"""Put the address book contacts inside a box on the map in the same group (API V5).

Calls :meth:`AddressBookV5.update_address_book_contact_by_areas
<route4me.address_book_v5.AddressBookV5.update_address_book_contact_by_areas>`, which sends
``PUT /modules/api/v5.0/address-book/addresses/update-by-areas`` (API V5, on ``wh.route4me.com``) with
the ``filter`` and the ``data`` to set as the JSON body, and prints where to follow the background job
that runs the update. This changes contacts of the account.

Run it with::

    python examples/addressbook/update_address_book_contact_by_areas.py --api_key <your key>
"""

import argparse

from route4me import Route4Me


def main(api_key):
    """Set the group of the contacts in the box and print the job.

    :param api_key: Route4Me API key.
    """
    route4me = Route4Me(api_key)

    address_book = route4me.address_book_v5
    response = address_book.update_address_book_contact_by_areas(
        filter={"bounding_box": {"top": 39.81, "left": -89.66, "bottom": 39.79, "right": -89.63}},
        data={"address_group": "Example group"},
    )
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    elif response == b"":
        reply = address_book.response
        print(f"Job queued (HTTP {reply.status_code}): {reply.headers.get('Location')}")
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update Address Book Contacts By Areas V5")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
