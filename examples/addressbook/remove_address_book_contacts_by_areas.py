r"""Delete the address book contacts inside a bounding box (API V5).

Calls :meth:`AddressBookV5.remove_address_book_contacts_by_areas
<route4me.address_book_v5.AddressBookV5.remove_address_book_contacts_by_areas>`, which sends
``DELETE /modules/api/v5.0/address-book/addresses/delete-by-areas`` (API V5, on ``wh.route4me.com``)
with the area as ``filter`` in the JSON body, and prints where to follow the background job.

Run it with::

    python examples/addressbook/remove_address_book_contacts_by_areas.py --api_key <your key> \
        --top <lat> --left <lng> --bottom <lat> --right <lng>
"""

import argparse

from route4me import Route4Me


def main(api_key, box):
    """Start the deletion and print the job.

    :param api_key: Route4Me API key.
    :param box: the bounding box, a dict with ``top``, ``left``, ``bottom`` and ``right``.
    """
    route4me = Route4Me(api_key)

    address_book = route4me.address_book_v5
    response = address_book.remove_address_book_contacts_by_areas(filter={"bounding_box": box})
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    elif response == b"":
        reply = address_book.response
        print(f"Job queued (HTTP {reply.status_code}): {reply.headers.get('Location')}")
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Remove Address Book Contacts by Areas (API V5)")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    for side in ("top", "left", "bottom", "right"):
        parser.add_argument(f"--{side}", dest=side, help=f"Edge of the box: {side}", type=float, required=True)
    args = parser.parse_args()
    main(args.api_key, {"top": args.top, "left": args.left, "bottom": args.bottom, "right": args.right})
