# -*- coding: utf-8 -*-

import os
import json
import datetime

import pytest
# import mock

import pytz

from route4me.sdk.self_test import MockerResourceWithNetworkClient
from .optimizations import Optimizations
import route4me.sdk.resources.optimizations as M

from route4me.sdk.utils import PagedList

from ..models import Optimization
from ..models import AlgorithmTypeEnum
from ..models import OptimizationStateEnum
from ..models import OptimizationFactorEnum

from ..errors import Route4MeApiError


class TestOptimizations(object):
	def test_ctor(self):

		api_key = '11111111111111111111111111111111'

		ns = Optimizations(api_key=api_key)

		assert ns is not None


class TestOptimizationApi(MockerResourceWithNetworkClient):

	resource_module = M

	def test_create(self):

		with open(os.path.join(
			# '..', '..', '..',
			'submodules', 'route4me-api-data-examples', 'Optimizations',
			'create_response.json'
		)) as f:
			sample_response_data = json.load(f)

		self.set_response(data=sample_response_data)

		o = Optimization()
		o.algorithm_type = AlgorithmTypeEnum.TSP
		o.state = OptimizationStateEnum.MATRIX_PROCESSING
		o.optimization_factor = OptimizationFactorEnum.DISTANCE
		o.route_datetime = datetime.datetime(2016, 6, 17)

		r = Optimizations(api_key='test')
		res = r.create(o)

		# print(self.mock_fluent_request_class.mock_calls)
		# call(),
		# call().method('POST'),
		# call().url('https://www.route4me.com//api.v4/optimization_problem.php'),
		# call().qs(None),
		# call().json({'links': {}, 'parameters': {'algorithm_type': 1}}),
		# call().user_agent('requests/2.18.3 (Linux 4.8.0-53-generic) Route4Me-Python-SDK/0.1.0 CPython/3.5.2'),
		# call().header('Route4Me-User-Agent', 'requests/2.18.3 (Linux 4.8.0-53-generic) ..'),
		# call().accept('application/json'),
		# call().header('Route4Me-Api-Key', 'test'),
		# call().qs({'format': 'json', 'api_key': 'test'}),
		# call().send(),
		# call().send().json()

		# ----------
		# assertions
		mock_freq = self.last_request()
		mock_freq.method.assert_called_with('POST')
		mock_freq.url.assert_called_with(
			'https://www.route4me.com/api.v4/optimization_problem.php'
		)
		mock_freq.json.assert_called_with(dict(o))

		# assertions on response
		assert isinstance(res, Optimization)
		assert res.ID == '1EDB78F63556D99336E06A13A34CF139'
		assert res.name == 'Fri, 17 Jun 2016 08:21:59 +0000 UTC'
		assert res.algorithm_type == AlgorithmTypeEnum.TSP
		assert res.state == OptimizationStateEnum.MATRIX_PROCESSING
		assert res.optimization_factor == OptimizationFactorEnum.DISTANCE
		assert res.member_id == '1'
		assert res.vehicle_id is None
		assert res.device_id is None

		assert res.route_datetime == datetime.datetime(2016, 6, 17, tzinfo=pytz.utc)

	def test_create_with_callback(self):

		with open(os.path.join(
			# '..', '..', '..',
			'submodules', 'route4me-api-data-examples', 'Optimizations',
			'create_response.json'
		)) as f:
			sample_response_data = json.load(f)

		self.set_response(data=sample_response_data)

		o = Optimization()
		o.algorithm_type = AlgorithmTypeEnum.TSP
		o.state = OptimizationStateEnum.MATRIX_PROCESSING
		o.optimization_factor = OptimizationFactorEnum.DISTANCE

		r = Optimizations(api_key='test')
		res = r.create(
			optimization_data=o,
			callback_url='https://callback.route4me.com/callback?q=1'
		)

		# ----------
		# assertions

		print(self.mock_fluent_request_class.mock_calls)
		# call(),
		# call().method('POST'),
		# call().url('https://www.route4me.com/api.v4/optimization_problem.php'),
		# call().qs({'optimized_callback_url': 'https://callback.route4me.com/callback?q=1'}),
		# call().json({'links': {}, 'parameters': {'store_route': True, 'algorithm_type': 1,
		# 	'route_max_duration': 86400, 'optimize': 'Distance'}, 'state': 2, 'addresses': []}),
		# call().user_agent('requests/2.18.3 (Linux 4.8.0-53-generic) Route4Me-Python-SDK/0.1.0 CPython/3.5.2'),
		# call().header('Route4Me-Agent',
		# 	'requests/2.18.3 (Linux 4.8.0-53-generic) Route4Me-Python-SDK/0.1.0 CPython/3.5.2'),
		# call().header('Route4Me-Agent-Release', '0.1.0-dev.5'),
		# call().header('Route4Me-Agent-Commit', None),
		# call().header('Route4Me-Agent-Build', None),
		# call().accept('application/json'),
		# call().header('Route4Me-Api-Key', 'test'),
		# call().qs({'api_key': 'test', 'format': 'json'}),
		# call().send(),
		# call().send().json()

		mock_freq = self.last_request()
		mock_freq.method.assert_called_with('POST')
		mock_freq.url.assert_called_with(
			'https://www.route4me.com/api.v4/optimization_problem.php'
		)
		mock_freq.json.assert_called_with(dict(o))
		mock_freq.qs.assert_any_call({
			'optimized_callback_url': 'https://callback.route4me.com/callback?q=1',
		})

		# assertions on response
		assert isinstance(res, Optimization)
		assert res.ID == '1EDB78F63556D99336E06A13A34CF139'

	def test_get(self):

		with open(os.path.join(
			# '..', '..', '..',
			'submodules', 'route4me-api-data-examples', 'Optimizations',
			'get_response.json'
		)) as f:
			sample_response_data = json.load(f)

		self.set_response(data=sample_response_data)

		r = Optimizations(api_key='test')
		res = r.get('07372F2CF3814EC6DFFAFE92E22771AA')

		print(self.mock_fluent_request_class.mock_calls)

		# ----------
		# assertions
		mock_freq = self.last_request()
		mock_freq.method.assert_called_with('GET')
		mock_freq.url.assert_called_with(
			'https://www.route4me.com/api.v4/optimization_problem.php'
		)
		mock_freq.qs.assert_any_call({
			'optimization_problem_id': '07372F2CF3814EC6DFFAFE92E22771AA'
		})
		assert not mock_freq.json.called
		assert not mock_freq.data.called

		# assertions on response
		assert isinstance(res, Optimization)
		assert res.ID == '07372F2CF3814EC6DFFAFE92E22771AA'
		assert res.name == 'Sunday 10th of April 2016 01:20 AM (+03:00)'
		assert res.algorithm_type == AlgorithmTypeEnum.CVRP_TW_SD
		assert res.state == OptimizationStateEnum.OPTIMIZED
		assert res.optimization_factor == OptimizationFactorEnum.TIME
		assert res.member_id == '44143'
		assert res.vehicle_id is None
		assert res.device_id is None
		assert res.round_trip is True

	def test_list_no_states(self):

		with open(os.path.join(
			# '..', '..', '..',
			'submodules', 'route4me-api-data-examples', 'Optimizations',
			'list_response.json'
		)) as f:
			sample_response_data = json.load(f)

		self.set_response(data=sample_response_data)

		r = Optimizations(api_key='test')
		res = r.list()

		print(self.mock_fluent_request_class.mock_calls)

		# ----------
		# assertions
		mock_freq = self.last_request()
		mock_freq.method.assert_called_with('GET')
		mock_freq.url.assert_called_with(
			'https://www.route4me.com/api.v4/optimization_problem.php'
		)
		mock_freq.qs.assert_any_call({})

		assert not mock_freq.json.called
		assert not mock_freq.data.called

		# assertions on response
		assert isinstance(res, list)
		assert isinstance(res, PagedList)
		assert res.total == 447
		assert res.limit is None
		assert res.offset is None

		res0 = res[0]
		assert isinstance(res0, Optimization)
		assert res0.ID == '7EC3FC88737C29E93A54E88243ACBC77'
		assert res0.name == 'Fri, 20 May 2016 12:43:46 +0000 UTC'
		assert res0.algorithm_type == AlgorithmTypeEnum.CVRP_TW_SD
		assert res0.state == OptimizationStateEnum.INITIAL
		assert res0.optimization_factor == OptimizationFactorEnum.DISTANCE
		assert res0.member_id == '1'
		assert res0.vehicle_id is None
		assert res0.device_id is None
		assert res0.round_trip is True

	def test_list_with_states(self):

		with open(os.path.join(
			# '..', '..', '..',
			'submodules', 'route4me-api-data-examples', 'Optimizations',
			'list_response.json'
		)) as f:
			sample_response_data = json.load(f)

		self.set_response(data=sample_response_data)

		r = Optimizations(api_key='test')
		res = r.list(states=[OptimizationStateEnum.INITIAL, OptimizationStateEnum.OPTIMIZED])

		print(self.mock_fluent_request_class.mock_calls)

		# ----------
		# assertions
		mock_freq = self.last_request()
		mock_freq.method.assert_called_with('GET')
		mock_freq.url.assert_called_with(
			'https://www.route4me.com/api.v4/optimization_problem.php'
		)
		mock_freq.qs.assert_any_call({
			'state': '1,4'
		})

		assert not mock_freq.json.called
		assert not mock_freq.data.called

		# assertions on response
		assert isinstance(res, list)
		assert isinstance(res, PagedList)
		assert res.total == 447
		assert res.limit is None
		assert res.offset is None

		res0 = res[0]
		assert isinstance(res0, Optimization)

	def test_remove(self):

		with open(os.path.join(
			# '..', '..', '..',
			'submodules', 'route4me-api-data-examples', 'Optimizations',
			'remove_response.json'
		)) as f:
			sample_response_data = json.load(f)

		self.set_response(data=sample_response_data)

		opt_id = 'DE62B03510AB5A6A876093F30F6C7BF5'
		r = Optimizations(api_key='test')
		res = r.remove(ID=opt_id)

		# print(self.mock_fluent_request_class.mock_calls)

		# ----------
		# assertions
		mock_freq = self.last_request()
		mock_freq.method.assert_called_with('DELETE')
		mock_freq.url.assert_called_with(
			'https://www.route4me.com/api.v4/optimization_problem.php'
		)
		mock_freq.qs.assert_any_call({
			'optimization_problem_id': opt_id
		})
		mock_freq.json.assert_called_once_with(None)

		assert not mock_freq.data.called

		assert res is True
		# assertions on response

	def test_remove_failed(self):

		self.set_response(data=None)

		opt_id = 'DE62B03510AB5A6A876093F30F6C7BF5'
		r = Optimizations(api_key='test')

		with pytest.raises(Route4MeApiError) as exc_info:
			r.remove(ID=opt_id)

		print(self.mock_fluent_request_class.mock_calls)

		exc = exc_info.value
		assert exc is not None

		# TODO: implement this!
		# assert exc.method == 'DELETE'
		# assert exc.url == 'https://www.route4me.com/api.v4/optimization_problem.php'
