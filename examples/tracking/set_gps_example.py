# -*- coding: utf-8 -*-

import argparse

from route4me import Route4Me

from route4me.constants import (
    FORMAT,
    DEVICE_TYPE
)


def main(api_key):
    route4me = Route4Me(api_key)
    route = route4me.route
    response = route.get_routes(limit=1, offset=0)
    if isinstance(response, dict) and 'errors' in response.keys():
        print('. '.join(response['errors']))
    else:
        gps = route4me.gps
        gps.format(FORMAT.JSON)
        gps.route_id(response[0]['route_id'])
        gps.lat(33.14384),
        gps.lng(-83.22466)
        gps.course(1)
        gps.speed(120)
        gps.device_type(DEVICE_TYPE.IPHONE, 'param')
        gps.member_id(1, 'param')
        gps.device_guid('TEST_GPS')
        gps.device_timestamp('2014-06-14 17:43:35')
        print(gps.params.keys())
        print(gps.set_gps_track())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Set GPS Tracking Data into a Route')
    parser.add_argument('--api_key', dest='api_key', help='Route4Me API KEY',
                        type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
