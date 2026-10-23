r"""Assign an optimization profile to a group of orders.

Calls :meth:`OrdersGroup.assign_optimization_profile
<route4me.orders_group.OrdersGroup.assign_optimization_profile>`, which sends
``POST /modules/api/v5.0/orders/aggregation/assign-optimization-profile`` (API V5, on
``wh.route4me.com``) with ``group_id`` and ``optimization_profile_id`` as the JSON body, and prints the
reply. get_orders_groups.py prints group IDs, and get_optimization_profiles.py profile IDs.

Run it with::

    python examples/orders_group/assign_optimization_profile_to_group.py --api_key <your key> \
        --group_id <group ID> --optimization_profile_id <profile ID>
"""

import argparse

from route4me import Route4Me


def main(api_key, group_id, optimization_profile_id):
    """Assign the profile to the group and print the reply.

    :param api_key: Route4Me API key.
    :param group_id: ID of the group of orders.
    :param optimization_profile_id: ID of the optimization profile.
    """
    r4m = Route4Me(api_key)
    orders_groups = r4m.orders_group

    data = orders_groups.assign_optimization_profile(optimization_profile_id, group_id)
    print(data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Assign Optimization Profile")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument(
        "--group_id", dest="group_id", help="ID of a group of orders, from get_orders_groups.py", required=True
    )
    parser.add_argument(
        "--optimization_profile_id",
        dest="optimization_profile_id",
        help="ID of an optimization profile, from get_optimization_profiles.py",
        required=True,
    )
    args = parser.parse_args()
    main(args.api_key, args.group_id, args.optimization_profile_id)
