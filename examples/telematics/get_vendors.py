"""List the telematics vendors Route4Me integrates with.

Calls :meth:`Telematics.get_vendors_v5 <route4me.telematics.Telematics.get_vendors_v5>`, which sends
``GET /modules/api/v5.0/telematics/vendors/all`` (API V5, on ``wh.route4me.com``). The vendors come
back under ``data``; each one is printed as ``key : value`` lines.

Run it with::

    python examples/telematics/get_vendors.py --api_key <your key>
"""

import argparse

from route4me import Route4Me


def main(api_key):
    """Print every telematics vendor.

    :param api_key: Route4Me API key.
    """
    route4me = Route4Me(api_key)

    telematics = route4me.telematics
    response = telematics.get_vendors_v5()
    if isinstance(response, dict) and "errors" in response.keys():
        print(response["errors"])
    else:
        for vendor in response.get("data", []):
            telematics.pp_response(vendor)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get Telematics Vendors")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
