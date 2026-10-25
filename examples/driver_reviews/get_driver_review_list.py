"""List the driver reviews.

Calls :meth:`DriverReviews.get_driver_review_list
<route4me.driver_reviews.DriverReviews.get_driver_review_list>`, which sends
``GET /modules/api/v5.0/driver-reviews`` (API V5, on ``wh.route4me.com``) with ``page`` and ``per_page``
in the query, and prints the first page.

Run it with::

    python examples/driver_reviews/get_driver_review_list.py --api_key <your key>
"""

import argparse

from route4me import Route4Me


def main(api_key):
    """Print the first page of the driver reviews.

    :param api_key: Route4Me API key.
    """
    route4me = Route4Me(api_key)

    response = route4me.driver_reviews.get_driver_review_list(page=1, per_page=10)
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get Driver Review List")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
