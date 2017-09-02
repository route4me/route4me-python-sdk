# -*- coding: utf-8 -*-

import pytest
# import mock

from .enums import OptimizationStateEnum
from .enums import TravelModeEnum


class TestPEnum(object):

	@pytest.mark.parametrize('value, exp', [
		('', []),
		([], []),

		('3', [OptimizationStateEnum.OPTIMIZING]),
		('3,4', [OptimizationStateEnum.OPTIMIZING, OptimizationStateEnum.OPTIMIZED]),

		(u'3', [OptimizationStateEnum.OPTIMIZING]),
		(u'3,4', [OptimizationStateEnum.OPTIMIZING, OptimizationStateEnum.OPTIMIZED]),

		(3, [OptimizationStateEnum.OPTIMIZING]),
		([3], [OptimizationStateEnum.OPTIMIZING]),
		([3, 4], [OptimizationStateEnum.OPTIMIZING, OptimizationStateEnum.OPTIMIZED]),

		(['3'], [OptimizationStateEnum.OPTIMIZING]),
		(['3', '4'], [OptimizationStateEnum.OPTIMIZING, OptimizationStateEnum.OPTIMIZED]),

		(OptimizationStateEnum.OPTIMIZING, [OptimizationStateEnum.OPTIMIZING]),
		([OptimizationStateEnum.OPTIMIZING], [OptimizationStateEnum.OPTIMIZING]),
		(
			[OptimizationStateEnum.OPTIMIZING, OptimizationStateEnum.OPTIMIZED],
			[OptimizationStateEnum.OPTIMIZING, OptimizationStateEnum.OPTIMIZED]
		),
	])
	def test_parse_many(self, value, exp):
		act = OptimizationStateEnum.parse_many(value)
		assert act == exp

	@pytest.mark.parametrize('value, exp', [
		('Walking', [TravelModeEnum.WALKING]),
		('Walking,Trucking', [TravelModeEnum.WALKING, TravelModeEnum.TRUCKING]),

		(u'Walking', [TravelModeEnum.WALKING]),
		(u'Walking,Trucking', [TravelModeEnum.WALKING, TravelModeEnum.TRUCKING]),

		(['Walking'], [TravelModeEnum.WALKING]),
		(['Walking', 'Trucking'], [TravelModeEnum.WALKING, TravelModeEnum.TRUCKING]),

		([u'Walking'], [TravelModeEnum.WALKING]),
		([u'Walking', u'Trucking'], [TravelModeEnum.WALKING, TravelModeEnum.TRUCKING]),
	])
	def test_parse_many_(self, value, exp):
		act = TravelModeEnum.parse_many(value)
		assert act == exp
