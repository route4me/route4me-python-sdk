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
        response = route.get_route(route_id=route_id)
        if isinstance(response, dict) and 'errors' in response.keys():
            print('. '.join(response['errors']))
        else:
            print('Original Route')
            print('Route ID: {}'.format(response['route_id']))
            for i, address in enumerate(response['addresses']):
                print('Address #{}'.format(i + 1))
                print('\tAddress: {0}'.format(address['address']))
                print('\tRoute Destination ID: {0}'.format(
                    address['route_destination_id']))
            route_destination_id = response['addresses'][1]['route_destination_id']
            route_destination_id2 = response['addresses'][2]['route_destination_id']
            data = {
                "route_destination_id": route_destination_id,
                "route_id": route_id,
                "addresses": [{
                    "route_destination_id": route_destination_id2,
                    "sequence_no": 6,
                }]
            }
            print('After Re-sequence Route')
            response = route.resequence_route(**data)
            print('Route ID: {}'.format(response['route_id']))
            for i, address in enumerate(response['addresses']):
                print('Address #{}'.format(i + 1))
                print('\tAddress: {0}'.format(address['address']))
                print('\tRoute Destination ID: {0}'.format(
                    address['route_destination_id']))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Re-sequence a Route')
    parser.add_argument('--api_key', dest='api_key', help='Route4Me API KEY',
                        type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
