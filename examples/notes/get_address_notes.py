# codebeat:disable[BLOCK_NESTING]
from route4me import Route4Me
from route4me.constants import *

KEY = "11111111111111111111111111111111"

def main():
    route4me = Route4Me(KEY)
    route = route4me.route
    response = route.get_routes(limit=10, Offset=5)
    if hasattr(response, 'errors'):
        print '. '.join(response.errors)
    else:
        response = route.get_route(route_id=response[0].route_id)
        if hasattr(response, 'errors'):
            print '. '.join(response.errors)
        else:
            route_id = response.route_id
            route_destination_id = response.addresses[0].route_destination_id
            response = route4me.address.get_address_notes(route_id=route_id,
                                                          route_destination_id=route_destination_id, )
            if hasattr(response, 'errors'):
                print '. '.join(response.errors)
            else:
                print 'Address: {}'.format(response.address)
                print 'Notes'
                for i, note in response.notes:
                    print '\t{0} - {1}'.format(i+1, note)

if __name__ == '__main__':
    main()
# codebeat:enable[BLOCK_NESTING]
