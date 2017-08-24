# -*- coding: utf-8 -*-

import os
import json

# import pytest
# import mock

from route4me.sdk.self_test import MockerResourceWithNetworkClient
from .optimizations import Optimizations
import route4me.sdk.resources.optimizations as M

from ..models import Optimization
from ..models import AlgorithmTypeEnum
from ..models import OptimizationStateEnum


class TestOptimizations:
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

		r = Optimizations(api_key='test')
		res = r.create(o)

		print(self.mock_fluent_request_class.mock_calls)
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
