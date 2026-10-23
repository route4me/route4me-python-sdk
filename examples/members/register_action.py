"""Register a new Route4Me account.

Calls :meth:`Members.register <route4me.members.Members.register>`, which sends
``POST /actions/register_action.php`` with ``plan`` in the query and the account fields as form data
(``strEmail``, ``strFirstName``, ``strLastName``, ``strIndustry``, ``chkTerms``, ``strPassword_1``,
``strPassword_2``, ``device_type`` and ``format``), and prints the reply. Running it registers the
sample email address; change the values first.

Run it with::

    python examples/members/register_action.py --api_key <your key>
"""

import argparse

from route4me import Route4Me


def main(api_key):
    """Register the sample account and print the reply.

    :param api_key: Route4Me API key.
    """
    route4me = Route4Me(api_key)

    members = route4me.members
    data = {
        "email_address": "john@example.com",
        "first_name": "Jhon",
        "last_name": "Route4Me",
        "check_terms": "1",
        "industry": "Python SDK",
        "device_type": "web",
        "plan": "enterprise_plan",
        "password_1": "ultrasecret",
        "password_2": "ultrasecret",
        "format": "json",
    }
    response = members.register(**data)
    if isinstance(response, dict) and "errors" in response.keys():
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Registering a New Member")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
