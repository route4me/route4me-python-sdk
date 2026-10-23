"""Find an asset by its tracking number.

Calls :meth:`AssetTracking.find_asset <route4me.asset_tracking.AssetTracking.find_asset>`, which
sends ``GET /api.v4/status.php`` with ``tracking`` in the query, and prints the reply: where the
asset is and its status.

Run it with::

    python examples/asset_tracking/find_asset.py --api_key <your key> --tracking <tracking number>
"""

import argparse
import json

from route4me import Route4Me


def main(api_key, tracking):
    """Print the asset.

    :param api_key: Route4Me API key.
    :param tracking: tracking number of the asset.
    """
    route4me = Route4Me(api_key)

    asset_tracking = route4me.asset_tracking
    response = asset_tracking.find_asset(tracking)
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(json.dumps(response, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find an Asset")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument("--tracking", dest="tracking", help="Tracking number", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key, args.tracking)
