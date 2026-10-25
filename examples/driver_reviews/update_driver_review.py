"""Change the comment of a driver review.

Calls :meth:`DriverReviews.update_driver_review
<route4me.driver_reviews.DriverReviews.update_driver_review>`, which sends
``PATCH /modules/api/v5.0/driver-reviews/{rating_id}`` (API V5, on ``wh.route4me.com``) with the new
``review`` as the JSON body, and prints the reply.

Run it with::

    python examples/driver_reviews/update_driver_review.py --api_key <your key> --rating_id <review ID>
"""

import argparse

from route4me import Route4Me


def main(api_key, rating_id):
    """Change the comment of the review and print the reply.

    :param api_key: Route4Me API key.
    :param rating_id: ID of the driver review.
    """
    route4me = Route4Me(api_key)

    response = route4me.driver_reviews.update_driver_review(rating_id, review="On time, and the driver was friendly")
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update Driver Review")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument("--rating_id", dest="rating_id", help="Driver review ID", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key, args.rating_id)
