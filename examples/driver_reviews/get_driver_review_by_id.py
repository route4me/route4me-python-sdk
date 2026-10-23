"""Get one driver review.

Calls :meth:`DriverReviews.get_driver_review_by_id
<route4me.driver_reviews.DriverReviews.get_driver_review_by_id>`, which sends
``GET /modules/api/v5.0/driver-reviews/{rating_id}`` (API V5, on ``wh.route4me.com``), and prints the
reply.

Run it with::

    python examples/driver_reviews/get_driver_review_by_id.py --api_key <your key> --rating_id <review ID>
"""

import argparse

from route4me import Route4Me


def main(api_key, rating_id):
    """Print the driver review.

    :param api_key: Route4Me API key.
    :param rating_id: ID of the driver review.
    """
    route4me = Route4Me(api_key)

    response = route4me.driver_reviews.get_driver_review_by_id(rating_id)
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get Driver Review By Id")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument("--rating_id", dest="rating_id", help="Driver review ID", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key, args.rating_id)
