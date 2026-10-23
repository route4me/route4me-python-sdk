"""Rename a schedule.

Calls :meth:`RecurringRoutes.update_schedule <route4me.recurring_routes.RecurringRoutes.update_schedule>`,
which sends ``PUT /modules/api/v5.0/recurring-routes/schedules/{schedule_uid}`` (API V5, on
``wh.route4me.com``) with the new name as the JSON body. Prints the reply.

Run it with::

    python examples/recurring_routes/update_schedule.py --api_key <your key> --schedule_uid <schedule_uid>
"""

import argparse

from route4me import Route4Me


def main(api_key, schedule_uid):
    """Rename the schedule and print the reply.

    :param api_key: Route4Me API key.
    :param schedule_uid: ID of the schedule.
    """
    route4me = Route4Me(api_key)

    response = route4me.recurring_routes.update_schedule(schedule_uid, name="Example schedule (updated)")
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update Schedule")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument("--schedule_uid", dest="schedule_uid", help="ID of the schedule", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key, args.schedule_uid)
