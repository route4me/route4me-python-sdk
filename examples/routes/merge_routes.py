# -*- coding: utf-8 -*-

from route4me import Route4Me

API_KEY = "11111111111111111111111111111111"


def main():
    r4m = Route4Me(API_KEY)
    route = r4m.route
    response = route.get_routes(limit=2, offset=0)
    if isinstance(response, dict) and 'errors' in response.keys():
        print('. '.join(response['errors']))
    else:
        route_id1 = response[0]['route_id']
        route_id2 = response[1]['route_id']
        data = {'route_ids': [route_id1, route_id2]}
        print('Routes to merge: {}'.format(data['route_ids']))
        response = route.merge_routes(**data)
        if isinstance(response, dict) and 'errors' in response.keys():
            print('. '.join(response['errors']))
        else:
            print('Optimization Problem ID: {}'.format(
                response['optimization_problem_id']
            ))
            print('Route ID: {}'.format(response['route_id']))
            for i, address in enumerate(response['addresses']):
                print('Address #{}'.format(i + 1))
                print('\tAddress: {0}'.format(address['address']))
                print('\tRoute Destination ID: {0}'.format(
                    address['route_destination_id']
                ))


if __name__ == '__main__':
    main()
