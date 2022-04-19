# -*- coding: utf-8 -*-
# codebeat:disable[BLOCK_NESTING]
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
        response = route.get_route(route_id=route_id)
        if isinstance(response, dict) and 'errors' in response.keys():
            print('. '.join(response['errors']))
        else:
            address = response['addresses'][0]
            route_destination_id = address['route_destination_id']
            response = route4me.address.get_address_notes(
                route_id=route_id,
                route_destination_id=route_destination_id,
            )
            if isinstance(response, dict) and 'errors' in response.keys():
                print('. '.join(response['errors']))
            else:
                print('Address: {}'.format(response['address']))
                print('Notes')
                for i, note in enumerate(response['notes']):
                    print('\t{0} - {1} - {2}'.format(i + 1, note['contents'], note['activity_type']))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Get Notes from an Address')
    parser.add_argument('--api_key', dest='api_key', help='Route4Me API KEY',
                        type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)

# codebeat:enable[BLOCK_NESTING]
