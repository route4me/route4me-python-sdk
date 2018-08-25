# -*- coding: utf-8 -*-

from route4me import Route4Me

API_KEY = "11111111111111111111111111111111"


def main():
    route4me = Route4Me(API_KEY)
    route = route4me.route
    response = route.get_routes(limit=10, offset=0)
    if isinstance(response, dict) and 'errors' in response.keys():
        print('. '.join(response['errors']))
    else:
        for i, route in enumerate(response):
            print('Route #{}'.format(i + 1))
            print('\tOptimization Problem ID: {}\tRoute ID: {}'.format(
                route['optimization_problem_id'], route['route_id']))


if __name__ == '__main__':
    main()
