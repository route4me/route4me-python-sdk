"""Register a member for a webinar.

Calls :meth:`Members.webinar_registration <route4me.members.Members.webinar_registration>`, which sends
``POST /actions/webinar_register.php`` with the contact details, ``member_id`` and ``webinar_date`` as
form fields, and prints the reply. The values are samples.

Run it with::

    python examples/members/webinar_registration.py --api_key <your key>
"""

import argparse

from route4me import Route4Me


def main(api_key):
    """Register the sample member and print the reply.

    :param api_key: Route4Me API key.
    """
    route4me = Route4Me(api_key)

    members = route4me.members
    data = {
        "email_address": "john@route4me.com",
        "first_name": "Jhon",
        "last_name": "Route4Me",
        "phone_number": "454-454544",
        "company_name": "Python SDK",
        "member_id": "123456",
        "webinar_date": "2016-09-16 02:48:00",
    }
    response = members.webinar_registration(**data)
    if isinstance(response, dict) and "errors" in response.keys():
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Webinar Registration")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
