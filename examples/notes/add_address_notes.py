# -*- coding: utf-8 -*-
import argparse

from route4me import Route4Me

from route4me.constants import (
    DEVICE_TYPE
)


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
            route_id = response['route_id']
            address = response['addresses'][0]
            route_destination_id = address['route_destination_id']
            lat = address['lat']
            lng = address['lng']
            note = 'Test Note Contents'
            response = route4me.address.add_address_notes(
                note,
                route_id=route_id,
                device_type=DEVICE_TYPE.WEB,
                activity_type='wrongdelivery',
                dev_lat=lat,
                dev_lng=lng,
                address_id=route_destination_id,
            )
            if isinstance(response, dict) and 'errors' in response.keys():
                print('. '.join(response['errors']))
            else:
                note = response['note']
                print('Note ID: {}'.format(response['note_id']))
                print('Note contents: {}'.format(note['contents']))
                print('Route ID: {}'.format(note['route_id']))
                print('Route Destination ID: {}'.format(
                    note['route_destination_id']
                ))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Add Address Notes')
    parser.add_argument('--api_key', dest='api_key', help='Route4Me API KEY',
                        type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
