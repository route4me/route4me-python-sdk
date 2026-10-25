"""Record a user license bought in a mobile app.

Calls :meth:`Members.app_purchase_user_license <route4me.members.Members.app_purchase_user_license>`,
which sends ``POST /api/member/user_license.php`` with ``member_id``, ``session_guid``, ``device_id``,
``device_type``, ``subscription_name``, ``token``, ``payload`` and ``format`` as the JSON body, and
prints the reply. The values are samples; a real call needs the member's session and the purchase token
and payload from the app store.

Run it with::

    python examples/members/app_purchase_user_license.py --api_key <your key>
"""

import argparse

from route4me import Route4Me


def main(api_key):
    """Send the sample license purchase and print the reply.

    :param api_key: Route4Me API key.
    """
    route4me = Route4Me(api_key)

    members = route4me.members
    data = {
        "member_id": 1,
        "session_guid": "454563",
        "device_id": "54564",
        "device_type": "ipad",
        "subscription_name": "IPAD_MONTHLY",
        "token": "4/P7q7W91a-oMsCeLvIaQm6bTrgtp7",
        "payload": "APA91bHun4MxP5egoKMwt2KZFBaFUH-1RYqx",
        "format": "json",
    }
    response = members.app_purchase_user_license(**data)
    if isinstance(response, dict) and "errors" in response.keys():
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="App Purchase user License")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
