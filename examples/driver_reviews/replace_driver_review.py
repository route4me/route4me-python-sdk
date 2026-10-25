r"""Replace a driver review.

Calls :meth:`DriverReviews.replace_driver_review
<route4me.driver_reviews.DriverReviews.replace_driver_review>`, which sends
``PUT /modules/api/v5.0/driver-reviews/{rating_id}`` (API V5, on ``wh.route4me.com``) with
``tracking_number``, ``rating`` and ``review`` as the JSON body, and prints the reply.

Run it with::

    python examples/driver_reviews/replace_driver_review.py --api_key <your key> \
        --rating_id <review ID> --tracking_number <tracking number>
"""

import argparse

from route4me import Route4Me


def main(api_key, rating_id, tracking_number):
    """Replace the review and print the reply.

    :param api_key: Route4Me API key.
    :param rating_id: ID of the driver review.
    :param tracking_number: Tracking number of the stop.
    """
    route4me = Route4Me(api_key)

    response = route4me.driver_reviews.replace_driver_review(
        rating_id, tracking_number=tracking_number, rating=4, review="Late, but the parcel was fine"
    )
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Replace Driver Review")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument("--rating_id", dest="rating_id", help="Driver review ID", type=str, required=True)
    parser.add_argument(
        "--tracking_number", dest="tracking_number", help="Tracking number of a stop", type=str, required=True
    )
    args = parser.parse_args()
    main(args.api_key, args.rating_id, args.tracking_number)
