"""Create an optimization from groups of orders.

Gets the order groups as get_orders_groups.py does, with :meth:`OrdersGroup.get_orders_group
<route4me.orders_group.OrdersGroup.get_orders_group>`
(``POST /modules/api/v5.0/orders/aggregation/combined``, API V5, on ``wh.route4me.com``), keeps the
groups that have orders and builds the optimization from them with
:meth:`Optimization.set_order_aggregation_groups
<route4me.optimization.Optimization.set_order_aggregation_groups>`, each group with its own optimization
profile, starting on 2024-06-10 (:meth:`Optimization.route_start_date_local
<route4me.optimization.Optimization.route_start_date_local>`). :meth:`Route4Me.run_optimization
<route4me.api.Route4Me.run_optimization>` sends ``POST /api.v4/optimization_problem.php``. Prints the
optimization link and the addresses of each route.

Run it with::

    python examples/orders_group/orders_groups_optimization.py --api_key <your key>
"""

import argparse

from route4me import Route4Me
from route4me.constants import ORDER_STATUS


def _print_groups(groups):
    """Print one line per group of orders.

    :param groups: the groups, from ``get_orders_group``.
    """
    for g in groups:
        print(
            " - ".join(
                [
                    f"GroupID: {g['group_id']}",
                    f"OptimizationProfileID: {g['optimization_profile_id']}",
                    f" GroupColumn: {g['group_column']}",
                    f"GroupValue: {g['group_value']}",
                    f"OrdersCount: {g['orders_count']}",
                ]
            )
        )


def main(api_key):
    """Build the optimization from the groups that have orders and print the routes.

    :param api_key: Route4Me API key.
    """
    r4m = Route4Me(api_key)
    orders_groups = r4m.orders_group

    scheduled_for_range = [
        "2024-06-01",
        "2024-06-10",
    ]

    statuses = [
        ORDER_STATUS.SCHEDULED,
    ]
    print("\nGetting Orders Groups:\n")
    groups = orders_groups.get_orders_group(scheduled_for_range, statuses)
    selected_groups = []
    _print_groups(groups)
    for g in groups:
        if g["orders_count"] > 0:
            selected_groups.append(g)
    print("\nSelected Groups:\n")
    _print_groups(selected_groups)

    if selected_groups:
        print("\nCreating Optimization with selected Groups:\n")
        optimization = r4m.optimization

        aggregations_id = []
        aggregation_profile_overrides = {}
        for g in selected_groups:
            aggregations_id.append(g["group_id"])
            aggregation_profile_overrides.update({g["group_id"]: g["optimization_profile_id"]})
        optimization.set_order_aggregation_groups(
            scheduled_for_range,
            aggregations_id,
            statuses,
            aggregation_profile_overrides,
        )
        optimization.route_start_date_local("2024-06-10")

        response = r4m.run_optimization()
        print(f"Optimization Link: {response['links']['view']}")
        for i, route in enumerate(response["routes"]):
            print(f"\t{i + 1}\tRoute Link: {route['links']['route']}")
            for address in route["addresses"]:
                print(f"\t\t\tAddress: {address['address']}")
    else:
        print("No matching orders found in the selected aggregations")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Optimization from Orders Groups")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
