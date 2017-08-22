# -*- coding: utf-8 -*-

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

	client = ApiClient('11111111111111111111111111111111')
	opt = Optimization()

	opt.algorithm_type = AlgorithmTypeEnum.TSP
	opt.share_route = False
	opt.store_route = False
	opt.route_time = False
	opt.route_max_duration = 24 * 60 * 60  # 24 hours (originally, in seconds)
	opt.vehicle_capacity = 1
	opt.vehicle_max_distance_mi = 10000
	opt.route_name = 'Optimization Example'
	opt.optimize = OptimizationFactorEnum.DISTANCE
	opt.distance_unit = DistanceUnitEnum.MI
	opt.device_type = DeviceTypeEnum.WEB
	opt.travel_mode = TravelModeEnum.DRIVING

	opt.addresses.append(Address(
		name='754 5th Ave New York, NY 10019',
		lat=40.7636197,
		lng=-73.9744388,
		alias='Bergdorf Goodman',
		is_depot=True,
		time=0
	))
	opt.addresses.append(Address(
		name='888 Madison Ave New York, NY 10014',
		lat=40.7715154,
		lng=-73.9669241,
		alias='Ralph Lauren Women\'s and Home',
		time=0
	))
	opt.addresses.append(Address(
		name='1011 Madison Ave New York, NY 10075',
		lat=40.7772129,
		lng=-73.9669,
		alias='Yigal Azrou\u00ebl',
		time=0
	))
	opt.addresses.append(Address(
		name='57 W 57th St New York, NY 10019',
		lat=40.7558695,
		lng=-73.9862019,
		alias='Verizon Wireless',
		time=0
	))

	opt = client.optimizations.create(opt)

	print('Optimization Link: {}'.format(opt.links.view))

	for address in opt.addresses:
		print('Route {0} \troute_id: {1}'.format(
			address.address,
			address.route_id
		))


if __name__ == '__main__':
	test_create_optimization()
