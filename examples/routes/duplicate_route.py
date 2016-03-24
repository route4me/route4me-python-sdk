#!/usr/bin/python

from route4me import Route4Me

KEY = "11111111111111111111111111111111"


def main():
    route4me = Route4Me(KEY)
    route = route4me.route
    response = route.get_routes(limit=10, Offset=5)
    if hasattr(response, 'errors'):
        print '. '.join(response.errors)
    else:
        response = route.duplicate_route(route_id=response[0].route_id)
        if hasattr(response, 'errors'):
            print '. '.join(response.errors)
        else:
            print 'Optimization Problem ID: {}'.format(response.optimization_problem_id)
            print 'Route ID: {}'.format(response.route_id)
            print 'Adresses'
            for i, address in enumerate(response.addresses):
                print '\t{0} - {1}'.format(i, address.address)

if __name__ == '__main__':
    main()
