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
        setGPS = route4me.setGPS
        setGPS.format(FORMAT.CSV)
        setGPS.route_id(response[0].route_id)
        setGPS.lat(33.14384),
        setGPS.lng(-83.22466)
        setGPS.course(1)
        setGPS.speed(120)
        setGPS.device_type(DEVICE_TYPE.IPHONE, 'param')
        setGPS.member_id(1, 'param')
        setGPS.device_guid('TEST_GPS')
        setGPS.device_timestamp('2014-06-14 17:43:35')
        print setGPS.params
        print setGPS.set_gps_params()


if __name__ == '__main__':
    main()
