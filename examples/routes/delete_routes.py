# -*- coding: utf-8 -*-

import argparse

from route4me import Route4Me


def main(api_key):
    route4me = Route4Me(api_key)

    route = route4me.route
    print('Getting Latest 2 Routes')
    response = route.get_routes(limit=2, offset=0)
    if isinstance(response, dict) and 'errors' in response.keys():
        print('. '.join(response['errors']))
    else:
        route_ids = [x['route_id'] for x in response]
        print('Route IDs: {}'.format(route_ids))
        if len(route_ids) > 0:
            response = route.delete_routes(route_id=route_ids)
            if hasattr(response, 'errors'):
                print('. '.join(response.errors))
            else:
                print('Routes Deleted:')
                for i, route in enumerate(response['route_ids']):
                    print('\t{0} - {1}'.format(i + 1, route))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Deleting Multiple Routes')
    parser.add_argument('--api_key', dest='api_key', help='Route4Me API KEY',
                        type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
