# -*- coding: utf-8 -*-
import argparse

from route4me import Route4Me

from route4me.constants import (
    ALGORITHM_TYPE,
    OPTIMIZE,
    DISTANCE_UNIT,
    DEVICE_TYPE,
    ADDRESS_STOP_TYPE,
)


# codebeat:disable[LOC, ABC]


def main(api_key):
    route4me = Route4Me(api_key)

    optimization = route4me.optimization
    address = route4me.address
    optimization.add({
        'algorithm_type': ALGORITHM_TYPE.CVRP_TW_SD,
        'share_route': 0,
        'route_name': 'Route with Pickup/Dropoff Feature and Capacity',
        'optimize': OPTIMIZE.DISTANCE,
        'distance_unit': DISTANCE_UNIT.MI,
        'device_type': DEVICE_TYPE.WEB,
        'vehicle_capacity': 6
    })
    address.add_address(
        address='151 Arbor Way Milledgeville GA 31061',
        alias='DEPOT',
        lat=33.132675170898,
        lng=-83.244743347168,
        is_depot=1,
        time=0
    )
    address.add_address(
        address='230 Arbor Way Milledgeville GA 31061',
        lat=33.129695892334,
        lng=-83.24577331543,
        pickup='PD_CUSTOMER001',
        alias='PICKUP CUSTOMER001',
        address_stop_type=ADDRESS_STOP_TYPE.PICKUP,
        original_route_id="ROUTE001",
        time=60
    )
    address.add_address(
        address='230 Arbor Way Milledgeville GA 31061',
        lat=33.129695892334,
        lng=-83.24577331543,
        pickup='PD_CUSTOMER002',
        original_route_id="ROUTE001",
        alias='PICKUP CUSTOMER002',
        address_stop_type=ADDRESS_STOP_TYPE.PICKUP,
        time=60
    )
    address.add_address(
        address='230 Arbor Way Milledgeville GA 31061',
        lat=33.129695892334,
        lng=-83.24577331543,
        pickup='PD_CUSTOMER003',
        original_route_id="ROUTE001",
        alias='PICKUP CUSTOMER003',
        address_stop_type=ADDRESS_STOP_TYPE.PICKUP,
        time=60
    )
    address.add_address(
        address='230 Arbor Way Milledgeville GA 31061',
        lat=33.129695892334,
        lng=-83.24577331543,
        pickup='PD_CUSTOMER004',
        original_route_id="ROUTE001",
        alias='PICKUP CUSTOMER004',
        address_stop_type=ADDRESS_STOP_TYPE.PICKUP,
        time=60
    )
    address.add_address(
        address='148 Bass Rd NE Milledgeville GA 31061',
        lat=33.143497,
        lng=-83.224487,
        dropoff='PD_CUSTOMER001',
        original_route_id="ROUTE001",
        alias='DROPOFF CUSTOMER001',
        address_stop_type=ADDRESS_STOP_TYPE.DELIVERY,
        time=60
    )
    address.add_address(
        address='117 Bill Johnson Rd NE Milledgeville GA 31061',
        lat=33.141784667969,
        lng=-83.237518310547,
        dropoff='PD_CUSTOMER002',
        original_route_id="ROUTE001",
        alias='DROPOFF CUSTOMER002',
        address_stop_type=ADDRESS_STOP_TYPE.DELIVERY,
        time=60
    )
    address.add_address(
        address='119 Bill Johnson Rd NE Milledgeville GA 31061',
        lat=33.141086578369,
        lng=-83.238258361816,
        dropoff='PD_CUSTOMER003',
        original_route_id="ROUTE001",
        alias='DROPOFF CUSTOMER003',
        address_stop_type=ADDRESS_STOP_TYPE.DELIVERY,
        time=60
    )
    address.add_address(
        address='131 Bill Johnson Rd NE Milledgeville GA 31061',
        lat=33.142036437988,
        lng=-83.238845825195,
        dropoff='PD_CUSTOMER004',
        original_route_id="ROUTE001",
        alias='DROPOFF CUSTOMER004',
        address_stop_type=ADDRESS_STOP_TYPE.DELIVERY,
        time=60
    )
    address.add_address(
        address='138 Bill Johnson Rd NE Milledgeville GA 31061',
        lat=33.14307,
        lng=-83.239334,
        pickup='PD_CUSTOMER005',
        original_route_id="ROUTE002",
        alias='PICKUP CUSTOMER005',
        address_stop_type=ADDRESS_STOP_TYPE.PICKUP,
        time=60
    )
    address.add_address(
        address='138 Bill Johnson Rd NE Milledgeville GA 31061',
        lat=33.14307,
        lng=-83.239334,
        pickup='PD_CUSTOMER006',
        original_route_id="ROUTE002",
        alias='PICKUP CUSTOMER006',
        address_stop_type=ADDRESS_STOP_TYPE.PICKUP,
        time=60
    )
    address.add_address(
        address='138 Bill Johnson Rd NE Milledgeville GA 31061',
        lat=33.14307,
        lng=-83.239334,
        pickup='PD_CUSTOMER007',
        original_route_id="ROUTE002",
        alias='PICKUP CUSTOMER007',
        address_stop_type=ADDRESS_STOP_TYPE.PICKUP,
        time=60
    )
    address.add_address(
        address='139 Bill Johnson Rd NE Milledgeville GA 31061',
        lat=33.142734527588,
        lng=-83.237442016602,
        dropoff='PD_CUSTOMER005',
        original_route_id="ROUTE002",
        alias='DROPOFF CUSTOMER005',
        address_stop_type=ADDRESS_STOP_TYPE.DELIVERY,
        time=60
    )
    address.add_address(
        address='145 Bill Johnson Rd NE Milledgeville GA 31061',
        lat=33.143871307373,
        lng=-83.237342834473,
        dropoff='PD_CUSTOMER006',
        original_route_id="ROUTE002",
        alias='DROPOFF CUSTOMER006',
        address_stop_type=ADDRESS_STOP_TYPE.DELIVERY,
        time=60
    )
    address.add_address(
        address='221 Blake Cir Milledgeville GA 31061',
        lat=33.081462860107,
        lng=-83.208511352539,
        dropoff='PD_CUSTOMER007',
        original_route_id="ROUTE002",
        alias='DROPOFF CUSTOMER007',
        address_stop_type=ADDRESS_STOP_TYPE.DELIVERY,
        time=60
    )
    response = route4me.run_optimization()
    print('Optimization Link: {}'.format(response['links']['view']))
    for i, route in enumerate(response['routes']):
        print('\t{0}\tRoute Link: {1}'.format(i + 1, route['links']['route']))
        for address in route['addresses']:
            print('\t\t\tAddress: {0}'.format(address['address']))


# codebeat:enable[LOC, ABC]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Route with Pickup/Dropoff Feature and Capacity')
    parser.add_argument('--api_key', dest='api_key', help='Route4Me API KEY',
                        type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
