"""Delete a schedule and keep its routes.

Calls :meth:`RecurringRoutes.delete_schedule <route4me.recurring_routes.RecurringRoutes.delete_schedule>`,
which sends ``DELETE /modules/api/v5.0/recurring-routes/schedules/{schedule_uid}`` (API V5, on
``wh.route4me.com``) with ``with-routes=0`` in the query. Prints the reply.

Run it with::

    python examples/recurring_routes/delete_schedule.py --api_key <your key> --schedule_uid <schedule_uid>
"""

import argparse

from route4me import Route4Me


def main(api_key, schedule_uid):
    """Delete the schedule and print the reply.

    :param api_key: Route4Me API key.
    :param schedule_uid: ID of the schedule.
    """
    route4me = Route4Me(api_key)

    response = route4me.recurring_routes.delete_schedule(schedule_uid, with_routes=False)
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Delete Schedule")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument("--schedule_uid", dest="schedule_uid", help="ID of the schedule", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key, args.schedule_uid)
