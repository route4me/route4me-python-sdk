# -*- coding: utf-8 -*-

import argparse

from route4me import Route4Me

from route4me.constants import OPTIMIZATION_STATE


def main(api_key):
    route4me = Route4Me(api_key)

    optimization = route4me.optimization
    response = optimization.get_optimizations(limit=10, offset=5)
    if hasattr(response, 'errors'):
        print('. '.join(response.errors))
    else:
        for i, optimization in enumerate(response['optimizations']):
            print('Optimization #{}'.format(i + 1))
            print('\tOptimization ID: {}'.format(
                optimization['optimization_problem_id']
            ))
            print('\tTotal Addresses: {}'.format(
                optimization['total_addresses']
            ))
            print('\tState: {}'.format(
                OPTIMIZATION_STATE.reverse_mapping.get(optimization['state'])
            ))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generic Optimization Example')
    parser.add_argument('--api_key', dest='api_key', help='Route4Me API KEY',
                        type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
