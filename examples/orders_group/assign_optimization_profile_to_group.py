# -*- coding: utf-8 -*-
# codebeat:disable[ABC]

import argparse

from route4me import Route4Me


def main(api_key):
    r4m = Route4Me(api_key)
    orders_groups = r4m.orders_group

    group_id = "ACE8FFFFFFFFFFFFFCCCCCCCCCCCCC"
    optimization_profile_id = "00000000-1111-1111-1111-000000000000"
    data = orders_groups.assign_optimization_profile(optimization_profile_id, group_id)
    print(data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Assign Optimization Profile")
    parser.add_argument(
        "--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True
    )
    args = parser.parse_args()
    main(args.api_key)

# codebeat:enable[ABC]
