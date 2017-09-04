# -*- coding: utf-8 -*-

import datetime

from route4me.sdk import ApiClient
from route4me.sdk.models import Optimization
from route4me.sdk.models import Address
from route4me.sdk.enums import (
	AlgorithmTypeEnum,
	OptimizationFactorEnum,
	DistanceUnitEnum,
	DeviceTypeEnum,
	TravelModeEnum,
)


def test_create_optimization():

	api = ApiClient('11111111111111111111111111111111')
	opt = Optimization()

	opt.algorithm_type = AlgorithmTypeEnum.TSP
	opt.travel_mode = TravelModeEnum.DRIVING
	opt.optimization_factor = OptimizationFactorEnum.DISTANCE
	opt.device_type = DeviceTypeEnum.WEB
	opt.share_route1 = False
	opt.store_route = False
	opt.route_datetime = datetime.datetime.now(tz=datetime.timezone.utc)
	opt.route_max_duration = 24 * 60 * 60  # 24 hours (originally, in seconds)
	opt.vehicle_capacity = 1
	opt.vehicle_max_distance_mi = 10000
	opt.route_name = 'Optimization Example'
	opt.distance_unit = DistanceUnitEnum.MILE

	addr = Address()
	addr.name = 'Bergdorf Goodman'
	addr.address = '754 5th Ave New York, NY 10019'
	addr.latitude = 40.7636197
	addr.longitude = -73.9744388
	addr.is_depot = True
	addr.service_time_sec = 0
	opt.addresses.append(addr)

	addr = Address()
	addr.name = 'Ralph Lauren Women\'s and Home'
	addr.address = '888 Madison Ave New York, NY 10014'
	addr.latitude = 40.7715154
	addr.longitude = -73.9669241
	addr.service_time_sec = 0
	opt.addresses.append(addr)

	addr = Address()
	addr.name = 'Yigal Azrou\u00ebl'
	addr.address = '1011 Madison Ave New York, NY 10075'
	addr.latitude = 40.7772129
	addr.longitude = -73.9669
	addr.service_time_sec = 0
	opt.addresses.append(addr)

	addr = Address()
	addr.name = 'Verizon Wireless'
	addr.address = '57 W 57th St New York, NY 10019'
	addr.latitude = 40.7558695
	addr.longitude = -73.9862019
	addr.service_time_sec = 0
	opt.addresses.append(addr)

	opt = api.optimizations.create(opt)

	print('Optimization Link: {}'.format(opt.links['view']))

	for address in opt.addresses:
		print('Route {0} \troute_id: {1}'.format(
			address.address,
			address.route_id
		))


if __name__ == '__main__':
	test_create_optimization()
