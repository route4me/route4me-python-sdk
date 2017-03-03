from route4me import Route4Me
from route4me.api_endpoints import ROUTE_HOST
from route4me.constants import (
    ALGORITHM_TYPE,
    OPTIMIZE,
    DISTANCE_UNIT,
    DEVICE_TYPE,
)

KEY = "11111111111111111111111111111111"


# codebeat:disable[LOC, ABC]


def main():
    route4me = Route4Me(KEY)
    optimization = route4me.optimization
    address = route4me.address
    optimization.add({
        'algorithm_type': ALGORITHM_TYPE.TSP,
        'share_route': 0,
        'route_name': 'Single Driver Route 10 Stops',
        'optimize': OPTIMIZE.DISTANCE,
        'distance_unit': DISTANCE_UNIT.MI,
        'device_type': DEVICE_TYPE.WEB,
    })
    address.add_address(
        address='151 Arbor Way Milledgeville GA 31061',
        lat=33.132675170898,
        lng=-83.244743347168,
        is_depot=1,
        time=0
    )
    address.add_address(
        address='230 Arbor Way Milledgeville GA 31061',
        lat=33.129695892334,
        lng=-83.24577331543,
        time=0
    )
    address.add_address(
        address='148 Bass Rd NE Milledgeville GA 31061',
        lat=33.143497,
        lng=-83.224487,
        time=0
    )
    address.add_address(
        address='117 Bill Johnson Rd NE Milledgeville GA 31061',
        lat=33.141784667969,
        lng=-83.237518310547,
        time=0
    )
    address.add_address(
        address='119 Bill Johnson Rd NE Milledgeville GA 31061',
        lat=33.141086578369,
        lng=-83.238258361816,
        time=0
    )
    address.add_address(
        address='131 Bill Johnson Rd NE Milledgeville GA 31061',
        lat=33.142036437988,
        lng=-83.238845825195,
        time=0
    )
    address.add_address(
        address='138 Bill Johnson Rd NE Milledgeville GA 31061',
        lat=33.14307,
        lng=-83.239334,
        time=0
    )
    address.add_address(
        address='139 Bill Johnson Rd NE Milledgeville GA 31061',
        lat=33.142734527588,
        lng=-83.237442016602,
        time=0
    )
    address.add_address(
        address='145 Bill Johnson Rd NE Milledgeville GA 31061',
        lat=33.143871307373,
        lng=-83.237342834473,
        time=0
    )
    address.add_address(
        address='221 Blake Cir Milledgeville GA 31061',
        lat=33.081462860107,
        lng=-83.208511352539,
        time=0
    )

    response = route4me.run_optimization()
    print('Optimization Link: {}'.format(response.links.view))
    for address in response.addresses:
        print('Route {0} link: {1} route_id={2}'.format(address.address,
                                                        ROUTE_HOST,
                                                        address.route_id))


# codebeat:enable[LOC, ABC]


if __name__ == '__main__':
    main()
