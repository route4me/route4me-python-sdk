# -*- coding: utf-8 -*-

import argparse

from route4me import Route4Me


def main(api_key):
    route4me = Route4Me(api_key)

    route = route4me.route
    response = route.get_routes(limit=10, offset=5)
    if isinstance(response, dict) and 'errors' in response.keys():
        print('. '.join(response['errors']))
    else:
        response = route.get_route(route_id=response[0]['route_id'])
        if isinstance(response, dict) and 'errors' in response.keys():
            print('. '.join(response['errors']))
        else:
            route_id = response['route_id']
            route_destination_id = response['addresses'][0]['route_destination_id']
            response = route4me.address.get_address(
                route_id=route_id,
                route_destination_id=route_destination_id)
            if isinstance(response, dict) and 'errors' in response.keys():
                print('. '.join(response['errors']))
            else:
                print('Address: {}'.format(response['address']))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Get an Address from a Route')
    parser.add_argument('--api_key', dest='api_key', help='Route4Me API KEY',
                        type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
