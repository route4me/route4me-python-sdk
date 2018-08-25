# -*- coding: utf-8 -*-

from route4me import Route4Me
from route4me.constants import OPTIMIZATION_STATE

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
        print('Re-optimization problem id: {}'.format(optimization_problem_id))
        response = route4me.re_optimization(optimization_problem_id)
        print('Re-optimization status: {}'.format(
            OPTIMIZATION_STATE.reverse_mapping.get(response['state'])))


if __name__ == '__main__':
    main()
