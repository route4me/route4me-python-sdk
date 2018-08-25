# -*- coding: utf-8 -*-

from route4me import Route4Me

API_KEY = "11111111111111111111111111111111"


def main():
    route4me = Route4Me(API_KEY)
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
    main()
