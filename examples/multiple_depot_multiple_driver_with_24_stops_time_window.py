from route4me import Route4Me
from route4me.api_endpoints import ROUTE_HOST
from route4me.constants import (
    ALGORITHM_TYPE,
    OPTIMIZE,
    DEVICE_TYPE,
    TRAVEL_MODE,
    DISTANCE_UNIT,
    METRIC,
)

KEY = '11111111111111111111111111111111'


# codebeat:disable[LOC, ABC]


def main():
    route4me = Route4Me(KEY)
    optimization = route4me.optimization
    address = route4me.address
    optimization.algorithm_type(ALGORITHM_TYPE.CVRP_TW_MD)
    optimization.share_route(0)
    optimization.store_route(0)
    optimization.route_time(0)
    optimization.route_max_duration(86400)
    optimization.vehicle_capacity(999)
    optimization.parts(20)
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
    address.add_address(
        address='3862 Klein Ave, Stow, OH 44224',
        lat=41.167895123363,
        lng=-81.429973393679,
        time=300,
        time_window_start=54379,
        time_window_end=54879
    )
    address.add_address(
        address='138 Northwood Ln, Tallmadge, OH 44278',
        lat=41.085464134812,
        lng=-81.447411775589,
        time=300,
        time_window_start=54879,
        time_window_end=56913
    )
    address.add_address(
        address='3401 Saratoga Blvd, Stow, OH 44224',
        lat=41.148849487305,
        lng=-81.407363891602,
        time=300,
        time_window_start=56913,
        time_window_end=57052
    )
    address.add_address(
        address='5169 Brockton Dr, Stow, OH 44224',
        lat=41.195003509521,
        lng=-81.392700195312,
        time=300,
        time_window_start=57052,
        time_window_end=59004
    )
    address.add_address(
        address='5169 Brockton Dr, Stow, OH 44224',
        lat=41.195003509521,
        lng=-81.392700195312,
        time=300,
        time_window_start=59004,
        time_window_end=60227
    )
    address.add_address(
        address='458 Aintree Dr, Munroe Falls, OH 44262',
        lat=41.1266746521,
        lng=-81.445808410645,
        time=300,
        time_window_start=60227,
        time_window_end=60375
    )
    address.add_address(
        address='512 Florida Pl, Barberton, OH 44203',
        lat=41.003671512008,
        lng=-81.598461046815,
        time=300,
        time_window_start=60375,
        time_window_end=63891
    )
    address.add_address(
        address='2299 Tyre Dr, Hudson, OH 44236',
        lat=41.250511169434,
        lng=-81.420433044434,
        time=300,
        time_window_start=63891,
        time_window_end=65277
    )
    address.add_address(
        address='2148 8th St, Cuyahoga Falls, OH 44221',
        lat=41.136692047119,
        lng=-81.493492126465,
        time=300,
        time_window_start=65277,
        time_window_end=68545
    )

    response = route4me.run_optimization()
    print('Optimization Link: {}'.format(response.links.view))
    for address in response.addresses:
        print('Route {0} link: {1}route_id: {2}'.format(address.address,
                                                        ROUTE_HOST,
                                                        address.route_id))


# codebeat:enable[LOC, ABC]


if __name__ == '__main__':
    main()
