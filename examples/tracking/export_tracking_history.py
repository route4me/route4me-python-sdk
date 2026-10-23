"""Export today's tracking history of a member as CSV, with API V5.

Calls :meth:`TrackingHistory.export_tracking_history
<route4me.tracking_history.TrackingHistory.export_tracking_history>` with ``member_id``,
``format="csv"`` and ``time_period="today"``, which sends
``POST /modules/api/v5.0/tracking-history/export`` (API V5, on ``wh.route4me.com``) with them as the
JSON body, and prints the CSV file.

Run it with::

    python examples/tracking/export_tracking_history.py --api_key <your key> --member_id <member ID>
"""

import argparse

from route4me import Route4Me


def main(api_key, member_id):
    """Print today's tracking history of the member.

    :param api_key: Route4Me API key.
    :param member_id: ID of the member.
    """
    route4me = Route4Me(api_key)

    tracking_history = route4me.tracking_history
    response = tracking_history.export_tracking_history(member_id=member_id, format="csv", time_period="today")
    if isinstance(response, bytes):
        print(response.decode("utf-8", errors="replace"))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Export Tracking History")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument("--member_id", dest="member_id", help="Member ID", type=int, required=True)
    args = parser.parse_args()
    main(args.api_key, args.member_id)
