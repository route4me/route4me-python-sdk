"""Optimize a round trip built from orders.

Creates five orders with :meth:`Order.create_order <route4me.orders.Order.create_order>`
(``POST /api.v4/order.php``), adds each to the optimization by its ``order_id`` with
:meth:`Address.add_address <route4me.address.Address.add_address>`, adds a depot, and runs a CVRP_TW_SD
round trip (``rt``) optimized for time with :meth:`Route4Me.run_optimization
<route4me.api.Route4Me.run_optimization>` (``POST /api.v4/optimization_problem.php``). The orders stay
in the account. Prints the optimization link and the addresses of each route.

Run it with::

    python examples/single_depot_round_trip_orders_based.py --api_key <your key>
"""

import argparse

from route4me import Route4Me
from route4me.constants import (
    ALGORITHM_TYPE,
    DEVICE_TYPE,
    DISTANCE_UNIT,
    OPTIMIZE,
    TRAVEL_MODE,
)


def main(api_key):
    """Create the orders, run the optimization and print the routes.

    :param api_key: Route4Me API key.
    """
    route4me = Route4Me(api_key)

    optimization = route4me.optimization
    address = route4me.address
    optimization.algorithm_type(ALGORITHM_TYPE.CVRP_TW_SD)
    optimization.share_route(0)
    optimization.store_route(0)
    optimization.route_time(0)
    optimization.rt(1)
    optimization.route_max_duration(86400)
    optimization.vehicle_max_distance_mi(10000)
    optimization.route_name("Single Depot Round Trip Orders Based")
    optimization.optimize(OPTIMIZE.TIME)
    optimization.distance_unit(DISTANCE_UNIT.MI)
    optimization.device_type(DEVICE_TYPE.WEB)
    optimization.travel_mode(TRAVEL_MODE.DRIVING)

    order_manager = route4me.order

    # Creating some Orders

    orders = [
        {
            "address_1": "754 5th Ave New York, NY 10019, USA",
            "address_stop_type": "DELIVERY",
            "day_scheduled_for_YYMMDD": "2022-12-24",
            "EXT_FIELD_cost": 5,
            "EXT_FIELD_pieces": 1,
            "EXT_FIELD_custom_data": {
                "attached_barcode": "ORD0002ABC12301",
            },
        },
        {
            "address_1": "717 5th Ave New York, NY 10022",
            "address_stop_type": "DELIVERY",
            "day_scheduled_for_YYMMDD": "2022-12-24",
            "EXT_FIELD_cost": 1,
            "EXT_FIELD_pieces": 1,
            "EXT_FIELD_custom_data": {
                "attached_barcode": "ORD0002ABC12302",
            },
        },
        {
            "address_1": "888 Madison Ave New York, NY 10014",
            "address_stop_type": "DELIVERY",
            "day_scheduled_for_YYMMDD": "2022-12-24",
            "EXT_FIELD_cost": 2,
            "EXT_FIELD_pieces": 1,
            "EXT_FIELD_custom_data": {
                "attached_barcode": "ORD0002ABC12303",
            },
        },
        {
            "address_1": "1011 Madison Ave New York, NY 10075",
            "address_stop_type": "DELIVERY",
            "day_scheduled_for_YYMMDD": "2022-12-24",
            "EXT_FIELD_cost": 6,
            "EXT_FIELD_pieces": 1,
            "EXT_FIELD_custom_data": {
                "attached_barcode": "ORD0002ABC12304",
            },
        },
        {
            "address_1": "440 Columbus Ave New York, NY 10024",
            "address_stop_type": "DELIVERY",
            "day_scheduled_for_YYMMDD": "2022-12-24",
            "EXT_FIELD_cost": 3,
            "EXT_FIELD_pieces": 1,
            "EXT_FIELD_custom_data": {
                "attached_barcode": "ORD0002ABC12305",
            },
        },
    ]

    for o in orders:
        new_order = order_manager.create_order(**o)
        address.add_address(order_id=new_order.get("order_id"))

    # Adding Depot

    address.add_address(
        address="57 W 57th St New York, NY 10019",
        lat=40.7558695,
        lng=-73.9862019,
        alias="Verizon Wireless",
        time=0,
        is_depot=True,
    )

    response = route4me.run_optimization()
    print(f"Optimization Link: {response['links']['view']}")
    for i, route in enumerate(response["routes"]):
        print(f"\t{i + 1}\tRoute Link: {route['links']['route']}")
        for address in route["addresses"]:
            print(f"\t\t\tAddress: {address['address']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Single Depot Round Trip, Orders Based")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
