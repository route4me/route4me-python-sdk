#!/usr/bin/python

from route4me import Route4Me
from route4me.constants import *

KEY = "11111111111111111111111111111111"


def main():
    route4me = Route4Me(KEY)
    optimization = route4me.optimization
    address = route4me.address
    optimization.algorithm_type(ALGORITHM_TYPE.CVRP_TW_SD)
    optimization.share_route(0)
    optimization.store_route(0)
    optimization.route_time(0)
    optimization.route_max_duration(86400)
    optimization.vehicle_capacity(1)
    optimization.vehicle_max_distance_mi(10000)
    optimization.route_name('Multiple Depot, Multiple Driver')
    optimization.optimize(OPTIMIZE.DISTANCE)
    optimization.distance_unit(DISTANCE_UNIT.MI)
    optimization.device_type(DEVICE_TYPE.WEB)
    optimization.travel_mode(TRAVEL_MODE.DRIVING)
    optimization.metric(METRIC.ROUTE4ME_METRIC_GEODESIC)
    address.add_address(
        address='3634 W Market St, Fairlawn, OH 44333',
        lat=41.135762259364,
        lng=-81.629313826561,
        is_depot=1,
        time=300,
        time_window_start=28800,
        time_window_end=29465
    )
    address.add_address(
        address='1218 Ruth Ave, Cuyahoga Falls, OH 44221',
        lat=41.143505096435,
        lng=-81.46549987793,
        time=300,
        time_window_start=29465,
        time_window_end=30529
    )
    address.add_address(
        address='512 Florida Pl, Barberton, OH 44203',
        lat=41.003671512008,
        lng=-81.598461046815,
        time=300,
        time_window_start=30529,
        time_window_end=33779
    )
    address.add_address(
        address='512 Florida Pl, Barberton, OH 44203',
        lat=41.003671512008,
        lng=-81.598461046815,
        time=300,
        time_window_start=33779,
        time_window_end=33944
    )
    address.add_address(
        address='3495 Purdue St, Cuyahoga Falls, OH 44221',
        lat=41.162971496582,
        lng=-81.479049682617,
        time=300,
        time_window_start=33944,
        time_window_end=34801
    )
    address.add_address(
        address='1659 Hibbard Dr, Stow, OH 44224',
        lat=41.194505989552,
        lng=-81.443351581693,
        time=300,
        time_window_start=34801,
        time_window_end=36366
    )
    address.add_address(
        address='2705 N River Rd, Stow, OH 44224',
        lat=41.145240783691,
        lng=-81.410247802734,
        time=300,
        time_window_start=36366,
        time_window_end=39173
    )
    address.add_address(
        address='10159 Bissell Dr, Twinsburg, OH 44087',
        lat=41.340042114258,
        lng=-81.421226501465,
        time=300,
        time_window_start=39173,
        time_window_end=41617
    )
    address.add_address(
        address='367 Cathy Dr, Munroe Falls, OH 44262',
        lat=41.148578643799,
        lng=-81.429229736328,
        time=300,
        time_window_start=41617,
        time_window_end=43660
    )
    address.add_address(
        address='367 Cathy Dr, Munroe Falls, OH 44262',
        lat=41.148579,
        lng=-81.42923,
        time=300,
        time_window_start=43660,
        time_window_end=46392
    )
    address.add_address(
        address='512 Florida Pl, Barberton, OH 44203',
        lat=41.003671512008,
        lng=-81.598461046815,
        time=300,
        time_window_start=46392,
        time_window_end=48389
    )
    address.add_address(
        address='559 W Aurora Rd, Northfield, OH 44067',
        lat=41.315116882324,
        lng=-81.558746337891,
        time=300,
        time_window_start=48389,
        time_window_end=48449
    )
    address.add_address(
        address='3933 Klein Ave, Stow, OH 44224',
        lat=41.169467926025,
        lng=-81.429420471191,
        time=300,
        time_window_start=48449,
        time_window_end=50152
    )
    address.add_address(
        address='2148 8th St, Cuyahoga Falls, OH 44221',
        lat=41.136692047119,
        lng=-81.493492126465,
        time=300,
        time_window_start=50152,
        time_window_end=51982
    )
    address.add_address(
        address='3731 Osage St, Stow, OH 44224',
        lat=41.161357879639,
        lng=-81.42293548584,
        time=300,
        time_window_start=51982,
        time_window_end=52180
    )
    address.add_address(
        address='3731 Osage St, Stow, OH 44224',
        lat=41.161357879639,
        lng=-81.42293548584,
        time=300,
        time_window_start=52180,
        time_window_end=54379
    )
    print optimization.data

    response = route4me.run_optimization()
    print 'Optimization Link: %s' % response.links.view
    for address in response.addresses:
        print 'Route %s link: %sroute_id=%s' % (address.address,
                                                route4me.route_url(),
                                                address.route_id)
    route4me.export_result_to_json('multiple_depot_multiple_driver.json')


if __name__ == '__main__':
    main()
