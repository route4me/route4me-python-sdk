"""Get one telematics vendor by ID.

Calls :meth:`Telematics.get_vendor_v5 <route4me.telematics.Telematics.get_vendor_v5>`, which sends
``GET /modules/api/v5.0/telematics/vendors`` with ``vendor_id`` in the query (API V5, on
``wh.route4me.com``), and prints the vendor as ``key : value`` lines: its name, title, the credentials
a connection needs and the entities it can sync. get_vendors.py prints the vendor IDs.

Run it with::

    python examples/telematics/get_vendor.py --api_key <your key> --vendor_id <vendor ID>
"""

import argparse

from route4me import Route4Me


def main(api_key, vendor_id):
    """Print one telematics vendor.

    :param api_key: Route4Me API key.
    :param vendor_id: ID of the vendor.
    """
    route4me = Route4Me(api_key)

    telematics = route4me.telematics
    vendor = telematics.get_vendor_v5(vendor_id)
    if isinstance(vendor, dict) and "errors" in vendor.keys():
        print(vendor["errors"])
    else:
        telematics.pp_response(vendor)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get a Telematics Vendor")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument("--vendor_id", dest="vendor_id", help="Telematics Vendor ID", type=int, required=True)
    args = parser.parse_args()
    main(args.api_key, args.vendor_id)
