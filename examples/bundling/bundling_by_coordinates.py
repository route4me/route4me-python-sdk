# -*- coding: utf-8 -*-
from route4me import Route4Me
from route4me import Bundling, BUNDLING_MODE
from route4me.constants import (
    ALGORITHM_TYPE,
    OPTIMIZE,
    DEVICE_TYPE,
    TRAVEL_MODE,
    DISTANCE_UNIT,
)

API_KEY = "11111111111111111111111111111111"


def main():
    route4me = Route4Me(API_KEY, redirects=False)
    optimization = route4me.optimization
    address = route4me.address
    optimization.algorithm_type(ALGORITHM_TYPE.CVRP_TW_SD)
    optimization.share_route(0)
    optimization.store_route(0)
    optimization.route_time(8 * 3600)
    optimization.route_name('Bundling Stops per Address Coordinate')
    optimization.optimize(OPTIMIZE.TIME)
    optimization.distance_unit(DISTANCE_UNIT.MI)
    optimization.device_type(DEVICE_TYPE.WEB)
    optimization.travel_mode(TRAVEL_MODE.DRIVING)

    """
    Bundling
    """

    bundling = Bundling()
    bundling.mode = BUNDLING_MODE.BY_COORDINATES
    optimization.bundling(bundling.to_dict())

    address.add_address(
        address='754 5th Ave New York, NY 10019',
        lat=40.7636197,
        lng=-73.9744388,
        alias='Bergdorf Goodman',
        is_depot=1
    )
    address.add_address(
        address='717 5th Ave New York, NY 10022',
        lat=40.7669692,
        lng=-73.9693864,
        alias='Giorgio Armani',
        time=60,
    )
    address.add_address(
        address='888 Madison Ave New York, NY 10014',
        lat=40.7715154,
        lng=-73.9669241,
        alias='Ralph Lauren Women\'s and Home',
        time=60,
    )
    address.add_address(
        address='1011 Madison Ave New York, NY 10075 - Address 1',
        lat=40.7772129,
        lng=-73.9669,
        alias='Yigal Azrou\u00ebl',
        time=60,

    )
    address.add_address(
        address='1011 Madison Ave New York, NY 10075 - Address 2',
        lat=40.7772129,
        lng=-73.9669,
        alias='Yigal Azrou\u00ebl',
        time=60,

    )

    address.add_address(
        address='1011 Madison Ave New York, NY 10075 - Address 3',
        lat=40.7772129,
        lng=-73.9669,
        alias='Yigal Azrou\u00ebl',
        time=60,

    )
    address.add_address(
        address='440 Columbus Ave New York, NY 10024',
        lat=40.7808364,
        lng=-73.9732729,
        alias='Frank Stella Clothier',
        time=60,
    )
    address.add_address(
        address='440 Columbus Ave New York, NY 10024',
        lat=40.7808364,
        lng=-73.9732729,
        alias='Frank Stella Clothier',
        time=60,
    )
    address.add_address(
        address='440 Columbus Ave New York, NY 10024',
        lat=40.7808364,
        lng=-73.9732729,
        alias='Frank Stella Clothier',
        time=60,
    )
    address.add_address(
        address='324 Columbus Ave #1 New York, NY 10023',
        lat=40.7803123,
        lng=-73.9793079,
        alias='Liana',
        time=60,
    )
    address.add_address(
        address='110 W End Ave New York, NY 10023',
        lat=40.7753077,
        lng=-73.9861529,
        alias='Toga Bike Shop',
        time=60,
    )
    address.add_address(
        address='555 W 57th St New York, NY 10019',
        lat=40.7718005,
        lng=-73.9897716,
        alias='BMW of Manhattan',
        time=60,
    )
    address.add_address(
        address='57 W 57th St New York, NY 10019',
        lat=40.7558695,
        lng=-73.9862019,
        alias='Verizon Wireless',
        time=60,
    )

    response = route4me.run_optimization()
    print('Optimization Link: {}'.format(response['links']['view']))
    for i, route in enumerate(response['routes']):
        print('\t{0}\tRoute Link: {1}'.format(i + 1, route['links']['route']))
        for address in route['addresses']:
            print('\t\t\tAddress: {0}'.format(address['address']))


if __name__ == '__main__':
    main()
