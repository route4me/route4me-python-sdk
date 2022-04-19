# -*- coding: utf-8 -*-

import argparse
from route4me import Route4Me

from route4me.constants import (
    ALGORITHM_TYPE,
    OPTIMIZE,
    DEVICE_TYPE,
    TRAVEL_MODE,
    DISTANCE_UNIT,
)


# codebeat:disable[LOC, ABC]


def main(api_key):
    route4me = Route4Me(api_key)

    optimization = route4me.optimization
    address = route4me.address
    optimization.algorithm_type(ALGORITHM_TYPE.CVRP_TW_SD)
    optimization.share_route(0)
    optimization.store_route(0)
    optimization.route_time(7 * 3600)
    optimization.parts(20)
    optimization.route_max_duration(86400)
    optimization.route_name('Single Depot, Multiple Driver')
    optimization.optimize(OPTIMIZE.DISTANCE)
    optimization.distance_unit(DISTANCE_UNIT.MI)
    optimization.device_type(DEVICE_TYPE.WEB)
    optimization.travel_mode(TRAVEL_MODE.DRIVING)

    address.add_address(
        address="455 S 4th St, Louisville, KY 40202",
        lat=38.251698,
        lng=-85.757308,
        is_depot=1
    )
    address.add_address(
        address="1604 PARKRIDGE PKWY, Louisville, KY, 40214",
        lat=38.141598,
        lng=-85.793846,
        time=300,
    )
    address.add_address(
        address="1407 MCCOY, Louisville, KY, 40215",
        lat=38.202496,
        lng=-85.786514,
        time=300,
    )
    address.add_address(
        address="4805 BELLEVUE AVE, Louisville, KY, 40215",
        lat=38.178844,
        lng=-85.774864,
        time=300,
    )
    address.add_address(
        address="730 CECIL AVENUE, Louisville, KY, 40211",
        lat=38.248684,
        lng=-85.821121,
        time=300,
    )
    address.add_address(
        address="650 SOUTH 29TH ST UNIT 315, Louisville, KY, 40211",
        lat=38.251923,
        lng=-85.800034,
        time=300,
    )
    address.add_address(
        address="4629 HILLSIDE DRIVE, Louisville, KY, 40216",
        lat=38.176067,
        lng=-85.824638,
        time=300,
    )
    address.add_address(
        address="4738 BELLEVUE AVE, Louisville, KY, 40215",
        lat=38.179806,
        lng=-85.775558,
        time=300,
    )
    address.add_address(
        address="318 SO. 39TH STREET, Louisville, KY, 40212",
        lat=38.259335,
        lng=-85.815094,
        time=300,
    )
    address.add_address(
        address="1324 BLUEGRASS AVE, Louisville, KY, 40215",
        lat=38.179253,
        lng=-85.785118,
        time=300,
    )
    address.add_address(
        address="7305 ROYAL WOODS DR, Louisville, KY, 40214",
        lat=38.162472,
        lng=-85.792854,
        time=300,
    )
    address.add_address(
        address="1661 W HILL ST, Louisville, KY, 40210",
        lat=38.229584,
        lng=-85.783966,
        time=300,
    )
    address.add_address(
        address="3222 KINGSWOOD WAY, Louisville, KY, 40216",
        lat=38.210606,
        lng=-85.822594,
        time=300,
    )
    address.add_address(
        address="1922 PALATKA RD, Louisville, KY, 40214",
        lat=38.153767,
        lng=-85.796783,
        time=300,
    )
    address.add_address(
        address="1314 SOUTH 26TH STREET, Louisville, KY, 40210",
        lat=38.235847,
        lng=-85.796852,
        time=300,
    )
    address.add_address(
        address="2135 MCCLOSKEY AVENUE, Louisville, KY, 40210",
        lat=38.218662,
        lng=-85.789032,
        time=300,
    )
    address.add_address(
        address="1409 PHYLLIS AVE, Louisville, KY, 40215",
        lat=38.206154,
        lng=-85.781387,
        time=300,
    )
    address.add_address(
        address="4504 SUNFLOWER AVE, Louisville, KY, 40216",
        lat=38.187511,
        lng=-85.839149,
        time=300,
    )
    address.add_address(
        address="2512 GREENWOOD AVE, Louisville, KY, 40210",
        lat=38.241405,
        lng=-85.795059,
        time=300,
    )
    address.add_address(
        address="5500 WILKE FARM AVE, Louisville, KY, 40216",
        lat=38.166065,
        lng=-85.863319,
        time=300,
    )
    address.add_address(
        address="3640 LENTZ AVE, Louisville, KY, 40215",
        lat=38.193283,
        lng=-85.786201,
        time=300,
    )
    address.add_address(
        address="1020 BLUEGRASS AVE, Louisville, KY, 40215",
        lat=38.17952,
        lng=-85.780037,
        time=300,
    )
    address.add_address(
        address="123 NORTH 40TH ST, Louisville, KY, 40212",
        lat=38.26498,
        lng=-85.814156,
        time=300,
    )
    address.add_address(
        address="7315 ST ANDREWS WOODS CIRCLE UNIT 104, Louisville, KY, 40214",
        lat=38.151072,
        lng=-85.802867,
        time=300,
    )
    address.add_address(
        address="3210 POPLAR VIEW DR, Louisville, KY, 40216",
        lat=38.182594,
        lng=-85.849937,
        time=300,
    )
    address.add_address(
        address="4519 LOUANE WAY, Louisville, KY, 40216",
        lat=38.1754,
        lng=-85.811447,
        time=300,
    )
    address.add_address(
        address="6812 MANSLICK RD, Louisville, KY, 40214",
        lat=38.161839,
        lng=-85.798279,
        time=300,
    )
    address.add_address(
        address="1524 HUNTOON AVENUE, Louisville, KY, 40215",
        lat=38.172031,
        lng=-85.788353,
        time=300,
    )
    address.add_address(
        address="1307 LARCHMONT AVE, Louisville, KY, 40215",
        lat=38.209663,
        lng=-85.779816,
        time=300,
    )
    address.add_address(
        address="434 N 26TH STREET #2, Louisville, KY, 40212",
        lat=38.26844,
        lng=-85.791962,
        time=300,
    )
    address.add_address(
        address="678 WESTLAWN ST, Louisville, KY, 40211",
        lat=38.250397,
        lng=-85.80629,
        time=300,
    )
    address.add_address(
        address="2308 W BROADWAY, Louisville, KY, 40211",
        lat=38.248882,
        lng=-85.790421,
        time=300,
    )
    address.add_address(
        address="2332 WOODLAND AVE, Louisville, KY, 40210",
        lat=38.233579,
        lng=-85.794257,
        time=300,
    )
    address.add_address(
        address="1706 WEST ST. CATHERINE, Louisville, KY, 40210",
        lat=38.239697,
        lng=-85.783928,
        time=300,
    )
    address.add_address(
        address="1699 WATHEN LN, Louisville, KY, 40216",
        lat=38.216465,
        lng=-85.792397,
        time=300,
    )
    address.add_address(
        address="2416 SUNSHINE WAY, Louisville, KY, 40216",
        lat=38.186245,
        lng=-85.831787,
        time=300,
    )
    address.add_address(
        address="6925 MANSLICK RD, Louisville, KY, 40214",
        lat=38.158466,
        lng=-85.798355,
        time=300,
    )
    address.add_address(
        address="2707 7TH ST, Louisville, KY, 40215",
        lat=38.212438,
        lng=-85.785082,
        time=300,
    )
    address.add_address(
        address="2014 KENDALL LN, Louisville, KY, 40216",
        lat=38.179394,
        lng=-85.826668,
        time=300,
        time_window_start=51600,
        time_window_end=52200
    )
    address.add_address(
        address="612 N 39TH ST, Louisville, KY, 40212",
        lat=38.273354,
        lng=-85.812012,
        time=300,
    )
    address.add_address(
        address="2215 ROWAN ST, Louisville, KY, 40212",
        lat=38.261703,
        lng=-85.786781,
        time=300,
    )
    address.add_address(
        address="1826 W. KENTUCKY ST, Louisville, KY, 40210",
        lat=38.241611,
        lng=-85.78653,
        time=300,
    )
    address.add_address(
        address="1810 GREGG AVE, Louisville, KY, 40210",
        lat=38.224716,
        lng=-85.796211,
        time=300,
    )
    address.add_address(
        address="4103 BURRRELL DRIVE, Louisville, KY, 40216",
        lat=38.191753,
        lng=-85.825836,
        time=300,
    )
    address.add_address(
        address="359 SOUTHWESTERN PKWY, Louisville, KY, 40212",
        lat=38.259903,
        lng=-85.823463,
        is_depot=0,
        time=300,
    )
    address.add_address(
        address="2407 W CHESTNUT ST, Louisville, KY, 40211",
        lat=38.252781,
        lng=-85.792109,
        time=300,
    )
    address.add_address(
        address="225 S 22ND ST, Louisville, KY, 40212",
        lat=38.257616,
        lng=-85.786658,
        time=300,
    )
    address.add_address(
        address="1404 MCCOY AVE, Louisville, KY, 40215",
        lat=38.202122,
        lng=-85.786072,
        time=300,
    )
    address.add_address(
        address="117 FOUNT LANDING CT, Louisville, KY, 40212",
        lat=38.270061,
        lng=-85.799438,
        time=300,
    )
    address.add_address(
        address="5504 SHOREWOOD DRIVE, Louisville, KY, 40214",
        lat=38.145851,
        lng=-85.7798,
        time=300,
    )

    response = route4me.run_optimization()
    print('Optimization Link: {}'.format(response['links']['view']))
    for i, route in enumerate(response['routes']):
        print('\t{0}\tRoute Link: {1}'.format(i + 1, route['links']['route']))
        for address in route['addresses']:
            print('\t\t\tAddress: {0}'.format(address['address']))


# codebeat:enable[LOC, ABC]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Single Depot, Multiple Driver')
    parser.add_argument('--api_key', dest='api_key', help='Route4Me API KEY',
                        type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
