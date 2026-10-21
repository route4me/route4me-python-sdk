import argparse

from route4me import Route4Me


def main(api_key, group_id, optimization_profile_id):
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
