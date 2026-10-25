r"""Add a driver review for a stop.

Calls :meth:`DriverReviews.create_driver_review
<route4me.driver_reviews.DriverReviews.create_driver_review>`, which sends
``POST /modules/api/v5.0/driver-reviews`` (API V5, on ``wh.route4me.com``) with ``tracking_number``,
``rating`` and ``review`` as the JSON body, and prints the reply. The review stays on the account.

Run it with::

    python examples/driver_reviews/create_driver_review.py --api_key <your key> \
        --tracking_number <tracking number>
"""

import argparse

from route4me import Route4Me


def main(api_key, tracking_number):
    """Add a review for the stop and print the reply.

    :param api_key: Route4Me API key.
    :param tracking_number: Tracking number of the stop.
    """
    route4me = Route4Me(api_key)

    response = route4me.driver_reviews.create_driver_review(tracking_number=tracking_number, rating=5, review="On time")
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create Driver Review")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument(
        "--tracking_number", dest="tracking_number", help="Tracking number of a stop", type=str, required=True
    )
    args = parser.parse_args()
    main(args.api_key, args.tracking_number)
