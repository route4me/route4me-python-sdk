"""Create a schedule that repeats on Mondays, Wednesdays and Fridays.

Calls :meth:`RecurringRoutes.create_schedule <route4me.recurring_routes.RecurringRoutes.create_schedule>`,
which sends ``POST /modules/api/v5.0/recurring-routes/schedules`` (API V5, on ``wh.route4me.com``) with the
schedule as the JSON body. Prints the reply.

Run it with::

    python examples/recurring_routes/create_schedule.py --api_key <your key>
"""

import argparse

from route4me import Route4Me


def main(api_key):
    """Create the schedule and print the reply.

    :param api_key: Route4Me API key.
    """
    route4me = Route4Me(api_key)

    response = route4me.recurring_routes.create_schedule(
        name="Example schedule",
        schedule=[{"mode": "weekly", "enabled": True, "weekly": {"every": 1, "weekdays": [1, 3, 5]}}],
        advance_interval=1,
        advance_schedule_interval_days=7,
        timezone="UTC",
    )
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create Schedule")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
