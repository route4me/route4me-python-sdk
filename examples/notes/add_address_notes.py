#!/usr/bin/python

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
            lat = response.addresses[0].lat
            lng = response.addresses[0].lng
            note = 'Test Note Contents'
            response = route4me.address.add_address_notes(note, route_id=route_id,
                                                          device_type=DEVICE_TYPE.WEB,
                                                          activity_type='wrongdelivery',
                                                          dev_lat=lat,
                                                          dev_lng=lng,
                                                          address_id=route_destination_id,
                                                          )
            if hasattr(response, 'errors'):
                print '. '.join(response.errors)
            else:
                print 'Note ID: {}'.format(response.note_id)
                print 'Note contents: {}'.format(response.note.contents)
                print 'Route ID: {}'.format(response.note.route_id)
                print 'Route Destination ID: {}'.format(response.note.route_destination_id)

if __name__ == '__main__':
    main()
