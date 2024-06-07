# -*- coding: utf-8 -*-
# codebeat:disable[LOC, ABC]

import argparse

from route4me import Route4Me

from route4me.constants import (
    ALGORITHM_TYPE,
    OPTIMIZE,
    DISTANCE_UNIT,
    DEVICE_TYPE,
    TRAVEL_MODE,
)


def main(api_key):
    r4m = Route4Me(api_key)

    optimization = r4m.optimization
    address = r4m.address
    optimization.algorithm_type(ALGORITHM_TYPE.TSP)
    optimization.share_route(0)
    optimization.store_route(0)
    optimization.route_time(0)
    optimization.route_max_duration(86400)
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

    response = r4m.run_optimization()

    print('Current Addresses')
    for i, address in enumerate(response['addresses']):
        print('Number {}:'.format(i))
        print('\taddress: {}'.format(address['address']))
        print('\t')
    addresses = {
        'addresses': [
            {
                'address': '555 W 57th St New York, NY 10019',
                'lat': 40.7718005,
                'lng': -73.9897716,
                'alias': 'BMW of Manhattan',
                'sequence_no': 2,
                'time': 300,
            },
            {
                'address': '57 W 57th St New York, NY 10019',
                'lat': 40.7558695,
                'lng': -73.9862019,
                'alias': 'Verizon Wireless',
                'sequence_no': 5,
                'time': 300,
            }
        ]
    }

    route_id = response['addresses'][1]['route_id']

    print('Inserting addresses in Route: {}'.format(route_id))

    response = r4m.route.insert_address_into_route(addresses, route_id)
    print('Addresses after insert')
    for i, address in enumerate(response['addresses']):
        print('Number {}:'.format(i))
        print('\taddress: {}'.format(address['address']))
        print('\t')


# codebeat:enable[LOC, ABC]

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Insert an address to an existing route into specific position')
    parser.add_argument('--api_key', dest='api_key', help='Route4Me API KEY',
                        type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
