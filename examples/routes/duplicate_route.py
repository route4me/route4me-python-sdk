# -*- coding: utf-8 -*-

import argparse

from route4me import Route4Me


def main(api_key):
    route4me = Route4Me(api_key)

    route = route4me.route
    response = route.get_routes(limit=1, offset=0)
    if isinstance(response, dict) and 'errors' in response.keys():
        print('. '.join(response['errors']))
    else:
        route_id = response[0]['route_id']
        print('Route ID: {}'.format(route_id))
        response = route.duplicate_route(route_id=route_id)

        route_id = response.get('route_id')
        opt = response.get('optimization_problem_id')
        addresses = response.get('addresses', [])

        if isinstance(response, dict) and 'errors' in response.keys():
            print('. '.join(response['errors']))
        elif opt and route_id and addresses:
            print('Optimization Problem ID: {}'.format(opt))
            print('Route ID: {}'.format(route_id))
            for address in addresses:
                print('\t\t\tAddress: {0}'.format(address['address']))
        else:
            print('Duplicate Route failed...')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Duplicate a Route')
    parser.add_argument('--api_key', dest='api_key', help='Route4Me API KEY',
                        type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
