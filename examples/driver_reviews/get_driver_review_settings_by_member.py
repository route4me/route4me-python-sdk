"""Get the driver review settings of your account.

Calls :meth:`DriverReviews.get_driver_review_settings_by_member
<route4me.driver_reviews.DriverReviews.get_driver_review_settings_by_member>`, which sends
``GET /modules/api/v5.0/driver-reviews/settings/get-by-member`` (API V5, on ``wh.route4me.com``), and
prints the reply.

Run it with::

    python examples/driver_reviews/get_driver_review_settings_by_member.py --api_key <your key>
"""

import argparse

from route4me import Route4Me


def main(api_key):
    """Print the driver review settings.

    :param api_key: Route4Me API key.
    """
    route4me = Route4Me(api_key)

    response = route4me.driver_reviews.get_driver_review_settings_by_member()
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get Driver Review Settings By Member")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
