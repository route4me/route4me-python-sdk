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
        response = route.delete_routes(route_id=[response[0].route_id, ])
        if hasattr(response, 'errors'):
            print '. '.join(response.errors)
        else:
            print 'Routes Deleted:'
            for i, route in enumerate(response.route_ids):
                print '\t{0} - {1}'.format(i+1, route)

if __name__ == '__main__':
    main()
