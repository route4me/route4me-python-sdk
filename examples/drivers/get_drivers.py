"""List the drivers of the account.

Calls :meth:`Drivers.get_drivers <route4me.drivers.Drivers.get_drivers>`, which sends
``GET /api/drivers/view_drivers.php``, and prints the reply.

Run it with::

    python examples/drivers/get_drivers.py --api_key <your key>
"""

import argparse
import json

from route4me import Route4Me


def main(api_key):
    """Print the drivers.

    :param api_key: Route4Me API key.
    """
    route4me = Route4Me(api_key)

    drivers = route4me.drivers
    response = drivers.get_drivers()
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    elif isinstance(response, bytes):
        print(response.decode("utf-8", errors="replace"))
    else:
        print(json.dumps(response, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get Drivers")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
