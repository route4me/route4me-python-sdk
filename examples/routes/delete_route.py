# -*- coding: utf-8 -*-
import argparse

from route4me import Route4Me


def main(api_key):
    route4me = Route4Me(api_key)

    route = route4me.route
    print('Getting Last Route')
    response = route.get_routes(limit=1, offset=0)
    if isinstance(response, dict) and 'errors' in response.keys():
        print('. '.join(response['errors']))
    else:
        route_id = response[0]['route_id']
        print('Route ID: {}'.format(route_id))
        response = route.delete_route(route_id=route_id)
        if isinstance(response, dict) and 'errors' in response.keys():
            print('. '.join(response['errors']))
        else:
            print('Route Deleted:')
            print(response)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Delete a Route')
    parser.add_argument('--api_key', dest='api_key', help='Route4Me API KEY',
                        type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
