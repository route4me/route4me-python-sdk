# -*- coding: utf-8 -*-

from route4me import Route4Me

API_KEY = "11111111111111111111111111111111"


def main():
    route4me = Route4Me(API_KEY)
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
    main()
