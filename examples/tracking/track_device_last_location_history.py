# -*- coding: utf-8 -*-

import argparse
import datetime as dt

from route4me import Route4Me
from route4me.constants import (
    FORMAT,
    DEVICE_TYPE
)


def main(api_key):
    route4me = Route4Me(api_key)

    gps = route4me.gps
    route = route4me.route
    response = route.get_routes(limit=1, offset=0)
    if isinstance(response, dict) and 'errors' in response.keys():
        print('. '.join(response['errors']))
    else:
        route_id = response[0]['route_id']
        print('Route ID: {}'.format(route_id))
        gps.add(params={
            'format': FORMAT.JSON,
            'route_id': route_id,
            'lng': -109.0803888,
            'course': 1,
            'device_type': DEVICE_TYPE.IPHONE,
            'member_id': 1,
            'device_guid': 'qweqweqwe',
        })
        # SET GPS
        for i in range(4):
            gps.add(params={
                'speed': 120 + i,
                'device_timestamp': dt.datetime.strftime(dt.datetime.now(),
                                                         "%Y-%m-%d %H:%M:%S"),
                'lat': 41.8927521 + i,
            })
            print('GPS Params SET %s' % gps.set_gps_track())
        route.add(params={
            'route_id': route_id,
            'device_tracking_history': 1,
        })
        response = route.get_route()
        for history in response['tracking_history']:
            print('lng: {0} lat: {1} time: {2} speed: {3} '.format(
                history['lg'],
                history['lt'],
                history['ts_friendly'],
                history['s']
            ))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Get Tracking History')
    parser.add_argument('--api_key', dest='api_key', help='Route4Me API KEY',
                        type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
