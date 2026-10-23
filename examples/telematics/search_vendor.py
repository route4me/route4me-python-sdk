"""Search the telematics vendors with filters.

Calls :meth:`Telematics.get_vendors_v5 <route4me.telematics.Telematics.get_vendors_v5>` once per
search. Each call sends ``GET /modules/api/v5.0/telematics/vendors/all`` (API V5, on
``wh.route4me.com``) with one filter -- ``size``, ``feature``, ``country`` or the keyword ``search`` --
and ``page=1``, ``per_page=2``. The vendors found come back under ``data``.

Run it with::

    python examples/telematics/search_vendor.py --api_key <your key>
"""

import argparse

from route4me import Route4Me

#: Each search: a title to print, and the filter to send.
SEARCHES = (
    ("Global vendors", {"size": "global"}),
    ("Vendors with the Satellite feature", {"feature": "Satellite"}),
    ("Vendors in GB", {"country": "GB"}),
    ('Vendors matching "fleet"', {"search": "fleet"}),
)


def main(api_key):
    """Run each search and print the first two vendors it finds.

    :param api_key: Route4Me API key.
    """
    route4me = Route4Me(api_key)

    telematics = route4me.telematics
    for title, filters in SEARCHES:
        print(f"*** {title} ***")
        response = telematics.get_vendors_v5(page=1, per_page=2, **filters)
        if isinstance(response, dict) and "errors" in response.keys():
            print(response["errors"])
            continue
        for vendor in response.get("data", []):
            telematics.pp_response(vendor)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Search Telematics Vendors")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
