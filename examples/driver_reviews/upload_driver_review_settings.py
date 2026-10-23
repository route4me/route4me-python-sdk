"""Store the driver review settings of your account.

Calls :meth:`DriverReviews.upload_driver_review_settings
<route4me.driver_reviews.DriverReviews.upload_driver_review_settings>`, which sends
``POST /modules/api/v5.0/driver-reviews/settings/upload`` (API V5, on ``wh.route4me.com``) with
``question``, ``logo_background_color`` and, with ``--logo``, the logo image as a base64 string
(``logo_picture``) as the JSON body, and prints the reply. This changes the settings of the account.

Run it with::

    python examples/driver_reviews/upload_driver_review_settings.py --api_key <your key>

Optional: ``--logo <image path>``.
"""

import argparse
import base64
import pathlib

from route4me import Route4Me


def main(api_key, logo):
    """Store the review settings and print the reply.

    :param api_key: Route4Me API key.
    :param logo: Path of a logo image to upload, or ``None``.
    """
    route4me = Route4Me(api_key)

    settings = {"question": "How was your delivery?", "logo_background_color": "#000000"}
    if logo is not None:
        settings["logo_picture"] = base64.b64encode(pathlib.Path(logo).read_bytes()).decode("ascii")
    response = route4me.driver_reviews.upload_driver_review_settings(**settings)
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upload Driver Review Settings")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument("--logo", dest="logo", help="Path of a logo image", type=str, required=False)
    args = parser.parse_args()
    main(args.api_key, args.logo)
