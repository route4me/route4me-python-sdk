"""Get the profile of the member the API key belongs to, with API V5.

Calls :meth:`AccountProfile.get_account_profile <route4me.account_profile.AccountProfile.get_account_profile>`,
which sends ``GET /modules/api/v5.0/profile-api`` (API V5, on ``wh.route4me.com``), and prints the
member ID, the account owner's member ID and the email address.

Run it with::

    python examples/account_profile/get_account_profile.py --api_key <your key>
"""

import argparse

from route4me import Route4Me


def main(api_key):
    """Print the profile.

    :param api_key: Route4Me API key.
    """
    route4me = Route4Me(api_key)

    account_profile = route4me.account_profile
    response = account_profile.get_account_profile()
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(f"Member ID: {response.get('member_id')}")
        print(f"Root member ID: {response.get('root_member_id')}")
        print(f"Email: {response.get('email')}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get Account Profile (API V5)")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
