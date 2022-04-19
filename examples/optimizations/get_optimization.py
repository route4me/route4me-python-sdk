# -*- coding: utf-8 -*-

import argparse

from route4me import Route4Me


def main(api_key):
    route4me = Route4Me(api_key)

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
    parser = argparse.ArgumentParser(description='Get Optimization')
    parser.add_argument('--api_key', dest='api_key', help='Route4Me API KEY',
                        type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
