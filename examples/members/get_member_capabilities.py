"""Get the capabilities of the account.

Calls :meth:`Members.get_member_capabilities <route4me.members.Members.get_member_capabilities>`,
which sends ``GET /api/member/capabilities.php``, and prints the capabilities: the enabled features,
travel modes and licensed modules, and whether the account is commercial.

Run it with::

    python examples/members/get_member_capabilities.py --api_key <your key>
"""

import argparse
import json

from route4me import Route4Me


def main(api_key):
    """Print the capabilities of the account.

    :param api_key: Route4Me API key.
    """
    route4me = Route4Me(api_key)

    members = route4me.members
    response = members.get_member_capabilities()
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(json.dumps(response, indent=2) if isinstance(response, (dict, list)) else response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get Member Capabilities")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
