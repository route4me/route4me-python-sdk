"""Count the scheduled routes and orders per day for a month.

Calls :meth:`RecurringRoutes.get_schedule_calendar
<route4me.recurring_routes.RecurringRoutes.get_schedule_calendar>`, which sends
``GET /api/schedule_calendar_data.php`` (API V4) with the date range and the ``orders`` and ``routes_count``
flags in the query. Prints the reply.

Run it with::

    python examples/recurring_routes/get_schedule_calendar.py --api_key <your key> \\
        --date_from <date_from> \\
        --date_to <date_to>
"""

import argparse

from route4me import Route4Me


def main(api_key, date_from, date_to):
    """Print the calendar.

    :param api_key: Route4Me API key.
    :param date_from: First date, as YYYY-MM-DD.
    :param date_to: Last date, as YYYY-MM-DD.
    """
    route4me = Route4Me(api_key)

    response = route4me.recurring_routes.get_schedule_calendar(
        date_from_string=date_from,
        date_to_string=date_to,
        timezone_offset_minutes=0,
        orders=True,
        routes_count=True,
    )
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get Schedule Calendar")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument("--date_from", dest="date_from", help="First date, as YYYY-MM-DD", type=str, required=True)
    parser.add_argument("--date_to", dest="date_to", help="Last date, as YYYY-MM-DD", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key, args.date_from, args.date_to)
