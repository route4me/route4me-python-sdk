# -*- coding: utf-8 -*-

import argparse
from route4me import Route4Me


def main(api_key):
    r4m = Route4Me(api_key)

    route = r4m.route
    response = route.get_routes(limit=1, offset=0)
    if isinstance(response, dict) and 'errors' in response.keys():
        print('. '.join(response['errors']))
    else:
        route_id = response[0]['route_id']
        print('Route ID: {}'.format(route_id))
        response = route.get_route_tracking(route_id=route_id)
        if hasattr(response, 'errors'):
            print('. '.join(response.errors))
        else:
            print('Optimization Problem ID: {}'.format(
                response['optimization_problem_id']
            ))
            for i, address in enumerate(response['addresses']):
                print('Address #{}'.format(i + 1))
                print('\tAddress: {0}'.format(address['address']))
                print('\tRoute Destination ID: {0}'.format(
                    address['route_destination_id']))
            print('Tracking History: {}'.format(','.join(
                response['tracking_history'])))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Get Route Tracking Data')
    parser.add_argument('--api_key', dest='api_key', help='Route4Me API KEY',
                        type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
