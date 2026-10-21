import argparse

from route4me import Route4Me
from route4me.constants import ORDER_STATUS


def _print_groups(groups):
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
    parser = argparse.ArgumentParser(description="Get Orders Group")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
