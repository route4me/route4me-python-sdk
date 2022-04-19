# -*- coding: utf-8 -*-

# codebeat:disable[LOC, ABC, BLOCK_NESTING]
import argparse

from route4me import Route4Me


def main(api_key):
    route4me = Route4Me(api_key)

    optimization = route4me.optimization
    response = optimization.get_optimizations(limit=10, offset=5)
    if isinstance(response, dict) and 'errors' in response.keys():
        print('. '.join(response['errors']))
    else:
        optimizations = response['optimizations']
        optimization_problem_id = optimizations[0]['optimization_problem_id']
        response = optimization.get_optimization(
            optimization_problem_id=optimization_problem_id
        )
        if isinstance(response, dict) and 'errors' in response.keys():
            print('. '.join(response['errors']))
        else:
            print('Addresses to include')
            for i, address in enumerate(response['addresses']):
                print('Address #{}'.format(i + 1))
                print('\tAddress: {}'.format(address['address']))
                print('\tLatitude: {}'.format(address['lat']))
                print('\tLongitude: {}'.format(address['lng']))
                print('\tAlias: {}'.format(address['alias']))
            addresses = [
                {
                    'address': '555 W 57th St New York, NY 10019',
                    'lat': 40.7718005,
                    'lng': -73.9897716,
                    'alias': 'BMW of Manhattan',
                    'time': 300,
                },
                {
                    'address': '57 W 57th St New York, NY 10019',
                    'lat': 40.7558695,
                    'lng': -73.9862019,
                    'alias': 'Verizon Wireless',
                    'time': 300,
                }
            ]
            print('Addresses to include')
            for i, address in enumerate(addresses):
                print('Address #{}'.format(i + 1))
                print('\tAddress: {}'.format(address['address']))
                print('\tLatitude: {}'.format(address['lat']))
                print('\tLongitude: {}'.format(address['lng']))
                print('\tAlias: {}'.format(address['alias']))
            response = optimization.update_optimization(
                optimization_problem_id=optimization_problem_id,
                addresses=addresses,
                reoptimize=True
            )
            if isinstance(response, dict) and 'errors' in response.keys():
                print('. '.join(response['errors']))
            else:
                print('Current Addresses')
                for i, address in enumerate(response['addresses']):
                    print('Address #{}'.format(i + 1))
                    print('\tAddress: {}'.format(address['address']))
                    print('\tLatitude: {}'.format(address['lat']))
                    print('\tLongitude: {}'.format(address['lng']))
                    print('\tAlias: {}'.format(address['alias']))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Add address to Optimization')
    parser.add_argument('--api_key', dest='api_key', help='Route4Me API KEY',
                        type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)

# codebeat:enable[LOC, ABC, BLOCK_NESTING]
