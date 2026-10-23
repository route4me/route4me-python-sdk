"""Get the configuration of the route data table.

Calls :meth:`RoutesV5.get_route_data_table_config <route4me.routes_v5.RoutesV5.get_route_data_table_config>`,
which sends ``GET /modules/api/v5.0/routes/datatable/config`` (API V5, on ``wh.route4me.com``), and prints
the reply.

Run it with::

    python examples/routes_v5/get_route_data_table_config.py --api_key <your key>
"""

import argparse

from route4me import Route4Me


def main(api_key):
    """Print the route data table configuration.

    :param api_key: Route4Me API key.
    """
    route4me = Route4Me(api_key)

    response = route4me.routes_v5.get_route_data_table_config()
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get the Route Data Table Config (API V5)")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
