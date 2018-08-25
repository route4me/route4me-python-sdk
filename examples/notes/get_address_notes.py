# -*- coding: utf-8 -*-
# codebeat:disable[BLOCK_NESTING]

from route4me import Route4Me

API_KEY = "11111111111111111111111111111111"


def main():
    route4me = Route4Me(API_KEY)
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
    main()

# codebeat:enable[BLOCK_NESTING]
