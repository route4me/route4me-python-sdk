# -*- coding: utf-8 -*-
# codebeat:disable[ABC]

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
    _print_groups(groups)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get Orders Group")
    parser.add_argument(
        "--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True
    )
    args = parser.parse_args()
    main(args.api_key)

# codebeat:enable[ABC]
