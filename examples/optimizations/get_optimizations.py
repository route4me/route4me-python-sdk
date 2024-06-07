# -*- coding: utf-8 -*-

import argparse

from route4me import Route4Me


def main(api_key):
    route4me = Route4Me(api_key)

    optimization = route4me.optimization
    response = optimization.get_optimizations(limit=10, offset=0)
    if isinstance(response, dict) and 'errors' in response.keys():
        print('. '.join(response['errors']))
    else:
        print('Latest 10 Optimizations')
        for i, optimization in enumerate(response['optimizations']):
            optimization_problem_id = optimization['optimization_problem_id']
            print('{0}.-\tOptimization ID: {1} - \t{2}'.format(i + 1,
                                                               optimization_problem_id,
                                                               optimization['parameters']['route_name']))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Get Optimizations')
    parser.add_argument('--api_key', dest='api_key', help='Route4Me API KEY',
                        type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
