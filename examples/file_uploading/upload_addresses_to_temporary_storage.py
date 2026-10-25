"""Upload addresses as JSON for fast bulk geocoding.

Calls :meth:`FileUploading.upload_addresses_to_temporary_storage
<route4me.file_uploading.FileUploading.upload_addresses_to_temporary_storage>`, which sends
``POST /actions/upload/json-geocode.php`` with two sample addresses as ``{"rows": [...]}`` in the
JSON body, and prints the reply: the ID of the stored batch and the number of addresses in it.

Run it with::

    python examples/file_uploading/upload_addresses_to_temporary_storage.py --api_key <your key>
"""

import argparse
import json

from route4me import Route4Me


def main(api_key):
    """Upload the sample addresses and print the reply.

    :param api_key: Route4Me API key.
    """
    route4me = Route4Me(api_key)

    file_uploading = route4me.file_uploading
    rows = [
        {"ADDRESS": "1 Example Way", "CITY": "Springfield", "STATE": "IL", "ZIP": "62701"},
        {"ADDRESS": "2 Example Way", "CITY": "Springfield", "STATE": "IL", "ZIP": "62701"},
    ]
    response = file_uploading.upload_addresses_to_temporary_storage(rows)
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(json.dumps(response, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upload Addresses for Bulk Geocoding")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
