# codebeat:disable[BLOCK_NESTING]
from route4me import Route4Me
from route4me.constants import *

KEY = "11111111111111111111111111111111"

def main():
    r4m = Route4Me(KEY)
    route = r4m.route
    response = route.get_routes(limit=10, Offset=5)
    if hasattr(response, 'errors'):
        print '. '.join(response.errors)
    else:
        response = route.get_route(route_id=response[0].route_id)
        if hasattr(response, 'errors'):
            print '. '.join(response.errors)
        else:
            print 'Route ID: {}'.format(response.route_id)
            data = {"route_path_output": 'Points',
                    "route_id": response.route_id}
            response = route.get_route_path_points(**data)
            print 'Optimization Problem ID: {}'.format(response.optimization_problem_id)
            print 'Route ID: {}'.format(response.route_id)
            for i, address in enumerate(response.addresses):
                print 'Address #{}'.format(i)
                print '\tAddress: {0}'.format(address.address)
                print '\tRoute Destination ID: {0}'.format(address.route_destination_id)
                for i, path in enumerate(address.path_to_next):
                    print '\t{0} - \tlat: {1} \tlng: {2}'.format(i + 1, path.lat, path.lng)


if __name__ == '__main__':
    main()
# codebeat:enable[BLOCK_NESTING]
