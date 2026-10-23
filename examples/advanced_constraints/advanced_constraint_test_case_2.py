"""Advanced constraints: some addresses without tags.

Builds an ADVANCED_CVRP_TW optimization of nine New York addresses, one of them the depot, optimized for
time, and sets two :class:`~route4me.advanced_constraint.AdvancedConstraint` groups with
:meth:`Optimization.advanced_constraints <route4me.base.Base.advanced_constraints>`: 10 drivers tagged
``TAG001`` and ``TAG002``, available from 25200 to 75000 seconds after midnight (07:00 to 20:50), and 10
drivers tagged ``TAG003``, available from 45200 to 95000 (12:33 to 02:23 the next day). Five stops carry
the tags of the drivers who may serve them; the last three have no tags.

:meth:`Route4Me.run_optimization <route4me.api.Route4Me.run_optimization>` sends
``POST /api.v4/optimization_problem.php``. Prints the optimization link and the addresses of each route.

Run it with::

    python examples/advanced_constraints/advanced_constraint_test_case_2.py --api_key <your key>
"""

import argparse

from route4me import AdvancedConstraint, Route4Me
from route4me.constants import (
    ALGORITHM_TYPE,
    DEVICE_TYPE,
    DISTANCE_UNIT,
    OPTIMIZE,
    TRAVEL_MODE,
)


def main(api_key):
    """Run the optimization with tagged and untagged stops and print the routes.

    :param api_key: Route4Me API key.
    """
    route4me = Route4Me(api_key)

    optimization = route4me.optimization
    address = route4me.address
    optimization.algorithm_type(ALGORITHM_TYPE.ADVANCED_CVRP_TW)
    optimization.share_route(0)
    optimization.store_route(0)
    optimization.route_time(8 * 3600)
    optimization.route_name("Advanced Constraints - Some addresses without Tags")
    optimization.optimize(OPTIMIZE.TIME)
    optimization.distance_unit(DISTANCE_UNIT.MI)
    optimization.device_type(DEVICE_TYPE.WEB)
    optimization.travel_mode(TRAVEL_MODE.DRIVING)

    # Advanced constraints: two groups of 10 drivers each. A driver serves only the stops
    # whose tags match the group's, inside the group's time windows (seconds from midnight).
    advanced_constraint_1 = AdvancedConstraint()
    advanced_constraint_1.tags = ["TAG001", "TAG002"]
    advanced_constraint_1.members_count = 10
    advanced_constraint_1.available_time_windows.append([25200, 75000])

    advanced_constraint_2 = AdvancedConstraint()
    advanced_constraint_2.members_count = 10
    advanced_constraint_2.tags = ["TAG003"]
    advanced_constraint_2.available_time_windows.append([45200, 95000])

    optimization.advanced_constraints([advanced_constraint_1.to_dict(), advanced_constraint_2.to_dict()])

    address.add_address(
        address="754 5th Ave New York, NY 10019", lat=40.7636197, lng=-73.9744388, alias="Bergdorf Goodman", is_depot=1
    )
    address.add_address(
        address="717 5th Ave New York, NY 10022",
        lat=40.7669692,
        lng=-73.9693864,
        alias="Giorgio Armani",
        time=60,
        tags=["TAG001", "TAG002"],
    )
    address.add_address(
        address="888 Madison Ave New York, NY 10014",
        lat=40.7715154,
        lng=-73.9669241,
        alias="Ralph Lauren Women's and Home",
        time=60,
        tags=["TAG001", "TAG002"],
    )
    address.add_address(
        address="1011 Madison Ave New York, NY 10075",
        lat=40.7772129,
        lng=-73.9669,
        alias="Yigal Azrou\u00ebl",
        time=60,
        tags=["TAG003"],
    )
    address.add_address(
        address="440 Columbus Ave New York, NY 10024",
        lat=40.7808364,
        lng=-73.9732729,
        alias="Frank Stella Clothier",
        time=60,
        tags=["TAG003"],
    )
    address.add_address(
        address="324 Columbus Ave #1 New York, NY 10023",
        lat=40.7803123,
        lng=-73.9793079,
        alias="Liana",
        time=60,
        tags=["TAG003"],
    )
    address.add_address(
        address="110 W End Ave New York, NY 10023",
        lat=40.7753077,
        lng=-73.9861529,
        alias="Toga Bike Shop",
        time=60,
    )
    address.add_address(
        address="555 W 57th St New York, NY 10019",
        lat=40.7718005,
        lng=-73.9897716,
        alias="BMW of Manhattan",
        time=60,
    )
    address.add_address(
        address="57 W 57th St New York, NY 10019",
        lat=40.7558695,
        lng=-73.9862019,
        alias="Verizon Wireless",
        time=60,
    )

    response = route4me.run_optimization()
    print(f"Optimization Link: {response['links']['view']}")
    for i, route in enumerate(response["routes"]):
        print(f"\t{i + 1}\tRoute Link: {route['links']['route']}")
        for address in route["addresses"]:
            print(f"\t\t\tAddress: {address['address']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advanced Constraints - Some addresses without Tags")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
