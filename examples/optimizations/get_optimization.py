# -*- coding: utf-8 -*-

from route4me import Route4Me

API_KEY = "11111111111111111111111111111111"


def main():
    route4me = Route4Me(API_KEY)
    optimization = route4me.optimization
    response = optimization.get_optimizations(limit=1, offset=0)
    if isinstance(response, dict) and 'errors' in response.keys():
        print('. '.join(response['errors']))
    else:
        optimizations = response['optimizations']
        optimization_problem_id = optimizations[0]['optimization_problem_id']
        response = optimization.get_optimization(
            optimization_problem_id=optimization_problem_id)
        if isinstance(response, dict) and 'errors' in response.keys():
            print('. '.join(response['errors']))
        else:
            optimization_problem_id = response['optimization_problem_id']
            print('\tOptimization ID: {}'.format(optimization_problem_id))
            print('Optimization Link: {}'.format(response['links']['view']))
            for i, route in enumerate(response['routes']):
                print('\t{0}\tRoute Link: {1}'.format(i + 1, route['links']['route']))
                for address in route['addresses']:
                    print('\t\t\tAddress: {0}'.format(address['address']))


if __name__ == '__main__':
    main()
