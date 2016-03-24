#!/usr/bin/python

from route4me import Route4Me

KEY = "11111111111111111111111111111111"


def main():
    route4me = Route4Me(KEY)
    optimization = route4me.optimization
    response = optimization.get_optimizations(limit=10, Offset=5)
    if hasattr(response, 'errors'):
        print '. '.join(response.errors)
    else:
        print response
        for i, optimization in enumerate(response.optimizations):
            print 'Optimization #{}'.format(i+1)
            print '\tOptimization ID: {}'.format(optimization.optimization_problem_id)
            #     print '\tActivity Message: {}'.format(activity.activity_message)
            #     print '\tActivity Type: {}'.format(activity.activity_type)
            #     print '\tRoute ID: {}'.format(activity.route_id)
            #     print '\tRoute Name: {}'.format(activity.route_name)

if __name__ == '__main__':
    main()
