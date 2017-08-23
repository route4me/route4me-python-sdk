# -*- coding: utf-8 -*-

import os
import json

# import pytest
import mock

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
			sample_response = json.load(f)

		self.client.post.return_value = sample_response

		o = Optimization()
		o.algorithm_type = AlgorithmTypeEnum.TSP

		r = Optimizations(api_key='test')
		res = r.create(o)

		print(self.client.mock_calls)
		assert self.client.post.call_args == mock.call(
			'/api.v4/optimization_problem.php',
			json=dict(o),
			query=None,
			subdomain='www'
		)
		assert isinstance(res, Optimization)
		assert res.ID == '1EDB78F63556D99336E06A13A34CF139'
		assert res.name == 'Fri, 17 Jun 2016 08:21:59 +0000 UTC'
		assert res.algorithm_type == AlgorithmTypeEnum.TSP
		assert res.state == OptimizationStateEnum.MATRIX_PROCESSING
