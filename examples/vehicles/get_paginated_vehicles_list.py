"""List the first ten vehicles, one page at a time.

Calls :meth:`VehiclesV5.get_paginated_vehicles_list
<route4me.vehicles_v5.VehiclesV5.get_paginated_vehicles_list>`, which sends
``GET /modules/api/v5.0/vehicles/paginate`` (API V5, on ``wh.route4me.com``), and prints the reply.

Run it with::

    python examples/vehicles/get_paginated_vehicles_list.py --api_key <your key>
"""

import argparse

from route4me import Route4Me


def main(api_key):
    """Print the first page of ten vehicles.

    :param api_key: Route4Me API key.
    """
    route4me = Route4Me(api_key)

    response = route4me.vehicles_v5.get_paginated_vehicles_list(page=1, per_page=10)
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get Paginated Vehicles")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
