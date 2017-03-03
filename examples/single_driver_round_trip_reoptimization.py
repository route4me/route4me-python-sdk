from route4me import Route4Me
from route4me.api_endpoints import ROUTE_HOST
from route4me.constants import (
    ALGORITHM_TYPE,
    OPTIMIZE,
    DISTANCE_UNIT,
    DEVICE_TYPE,
    TRAVEL_MODE,
    OPTIMIZATION_STATE,
)

KEY = "11111111111111111111111111111111"


# codebeat:disable[LOC, ABC]


def main():
    route4me = Route4Me(KEY)
    api = route4me
    optimization = api.optimization
    address = api.address
    optimization.algorithm_type(ALGORITHM_TYPE.TSP)
    optimization.share_route(0)
    optimization.store_route(0)
    optimization.route_time(0)
    optimization.route_max_duration(86400)
    optimization.vehicle_capacity(1)
    optimization.vehicle_max_distance_mi(10000)
    optimization.route_name('Single Driver Round Trip')
    optimization.optimize(OPTIMIZE.DISTANCE)
    optimization.distance_unit(DISTANCE_UNIT.MI)
    optimization.device_type(DEVICE_TYPE.WEB)
    optimization.travel_mode(TRAVEL_MODE.DRIVING)
    address.add_address(
        address='754 5th Ave New York, NY 10019',
        lat=40.7636197,
        lng=-73.9744388,
        alias='Bergdorf Goodman',
        is_depot=1,
        time=0
    )
    address.add_address(
        address='717 5th Ave New York, NY 10022',
        lat=40.7669692,
        lng=-73.9693864,
        alias='Giorgio Armani',
        time=0
    )
    address.add_address(
        address='888 Madison Ave New York, NY 10014',
        lat=40.7715154,
        lng=-73.9669241,
        alias='Ralph Lauren Women\'s and Home',
        time=0
    )
    address.add_address(
        address='1011 Madison Ave New York, NY 10075',
        lat=40.7772129,
        lng=-73.9669,
        alias='Yigal Azrou\u00ebl',
        time=0
    )
    address.add_address(
        address='440 Columbus Ave New York, NY 10024',
        lat=40.7808364,
        lng=-73.9732729,
        alias='Frank Stella Clothier',
        time=0
    )
    address.add_address(
        address='324 Columbus Ave #1 New York, NY 10023',
        lat=40.7803123,
        lng=-73.9793079,
        alias='Liana',
        time=0
    )
    address.add_address(
        address='110 W End Ave New York, NY 10023',
        lat=40.7753077,
        lng=-73.9861529,
        alias='Toga Bike Shop',
        time=0
    )
    address.add_address(
        address='555 W 57th St New York, NY 10019',
        lat=40.7718005,
        lng=-73.9897716,
        alias='BMW of Manhattan',
        time=0
    )
    address.add_address(
        address='57 W 57th St New York, NY 10019',
        lat=40.7558695,
        lng=-73.9862019,
        alias='Verizon Wireless',
        time=0
    )

    response = route4me.run_optimization()
    print('Optimization status: {}'.format(
        OPTIMIZATION_STATE.reverse_mapping.get(response.state)
    ))
    print('Optimization Link: {}'.format(response.links.view))
    for address in response.addresses:
        print('Route {0} link: {1} route_id={2}'.format(
            address.address,
            ROUTE_HOST,
            address.route_id
        ))
    print('Re-optimization...')
    optimization_problem_id = response.optimization_problem_id
    response = api.reoptimization(optimization_problem_id)
    print('Re-optimization status: {}'.format(
        OPTIMIZATION_STATE.reverse_mapping.get(response.state)
    ))


# codebeat:enable[LOC, ABC]


if __name__ == '__main__':
    main()
