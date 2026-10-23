"""Move a route to another schedule.

Calls :meth:`RecurringRoutes.update_route_schedule
<route4me.recurring_routes.RecurringRoutes.update_route_schedule>`, which sends
``PUT /modules/api/v5.0/recurring-routes/route-schedules/{route_id}`` (API V5, on ``wh.route4me.com``) with
``route_uid``, ``schedule_uid`` and ``root_member_id`` as the JSON body. Prints the reply.

Run it with::

    python examples/recurring_routes/update_route_schedule.py --api_key <your key> \\
        --route_id <route_id> \\
        --schedule_uid <schedule_uid> \\
        --root_member_id <root_member_id>
"""

import argparse

from route4me import Route4Me


def main(api_key, route_id, schedule_uid, root_member_id):
    """Update the route schedule and print the reply.

    :param api_key: Route4Me API key.
    :param route_id: ID of the route.
    :param schedule_uid: ID of the new schedule.
    :param root_member_id: ID of the root member of the account.
    """
    route4me = Route4Me(api_key)

    response = route4me.recurring_routes.update_route_schedule(
        route_id,
        route_uid=route_id,
        schedule_uid=schedule_uid,
        root_member_id=root_member_id,
    )
    if isinstance(response, dict) and "errors" in response:
        print(". ".join(response["errors"]))
    else:
        print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update Route Schedule")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument("--route_id", dest="route_id", help="ID of the route", type=str, required=True)
    parser.add_argument("--schedule_uid", dest="schedule_uid", help="ID of the new schedule", type=str, required=True)
    parser.add_argument(
        "--root_member_id", dest="root_member_id", help="ID of the root member of the account", type=int, required=True
    )
    args = parser.parse_args()
    main(args.api_key, args.route_id, args.schedule_uid, args.root_member_id)
