from route4me import Route4Me
from route4me.constants import (
    FORMAT,
    DEVICE_TYPE
)

KEY = "11111111111111111111111111111111"


def main():
    route4me = Route4Me(KEY)
    route = route4me.route
    response = route.get_routes(limit=10, Offset=5)
    if hasattr(response, 'errors'):
        print('. '.join(response.errors))
    else:
        gps = route4me.gps
        gps.format(FORMAT.CSV)
        gps.route_id(response[0].route_id)
        gps.lat(33.14384),
        gps.lng(-83.22466)
        gps.course(1)
        gps.speed(120)
        gps.device_type(DEVICE_TYPE.IPHONE, 'param')
        gps.member_id(1, 'param')
        gps.device_guid('TEST_GPS')
        gps.device_timestamp('2014-06-14 17:43:35')
        print(gps.params)
        print(gps.set_gps_track())


if __name__ == '__main__':
    main()
