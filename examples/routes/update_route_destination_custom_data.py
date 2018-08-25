# -*- coding: utf-8 -*-

from route4me import Route4Me

API_KEY = "11111111111111111111111111111111"


def main():
    r4m = Route4Me(API_KEY)
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
            route_destination_id = response['addresses'][1]['route_destination_id']
            print('Route Destination ID: {}'.format(route_destination_id))
            data = {
                "route_destination_id": route_destination_id,
                "route_id": route_id,
                "custom_fields": {
                    "SDK": "Python"
                }
            }
            response = route.update_route_destination_custom_data(**data)
            print('Route ID: {}'.format(route_id))
            print('\tAddress: {0}'.format(response['address']))
            print('\tRoute Destination ID: {0}'.format(
                response['route_destination_id']
            ))
            print('\tCustom Fields: {0}'.format(response['custom_fields']))


if __name__ == '__main__':
    main()
