# -*- coding: utf-8 -*-

# import pytest
import mock

from . import TiedListWrapper

from . import Address
from . import Optimization


class TestTiedListWrapper_Existing_Address(object):

	parent = None
	mylist = None

	@classmethod
	def setup_method(cls, *args, **qw):
		cls.parent = Optimization(raw={
			'addresses': [
				{
					'lat': 1,
					'route_destination_id': 100
				},
				{
					'lat': 2,
					'route_destination_id': 200
				},
			]
		})

		cls.mylist = TiedListWrapper(
			parent=cls.parent,
			key='addresses',
			anytype=Address
		)

	@classmethod
	def teardown_method(cls, *args, **qw):
		cls.parent = None
		cls.mylist = None

	def test_iterator_on_existance_parent(self):

		exp = []
		cnt = 0
		m = mock.MagicMock()
		m.ID = 100
		m.latitude = 1.
		exp.append(m)

		m = mock.MagicMock()
		m.ID = 200
		m.latitude = 2.
		exp.append(m)

		for i in self.mylist:
			ee = exp[cnt]
			assert isinstance(i, Address)
			assert i.ID == ee.ID
			assert i.latitude == ee.latitude

			cnt += 1

	def test_append_model(self):

		addr = Address(raw={'route_destination_id': 123})

		self.mylist.append(addr)

		li = self.mylist

		assert len(li) == 3
		assert li[2] == addr

	def test_append_raw_dict(self):

		addr = {'route_destination_id': 123}

		self.mylist.append(addr)

		li = self.mylist

		assert len(li) == 3
		assert li[2] == addr

	def test_unlink(self):

		self.mylist.unlink()

		assert 'addresses' in self.parent.raw
		assert self.parent.raw['addresses'] is None

	def test_unset(self):

		self.mylist.unset()

		assert 'addresses' not in self.parent.raw


class TestOptimization(object):
	def test_links(self):
		opt = Optimization(raw={

			'optimization_problem_id': '1EDB78F63556D99336E06A13A34CF139',
			'user_errors': [],
			'optimization_errors': [],
			'state': 2,
			'created_timestamp': 1466151720,
			'scheduled_for': 1466121600,
			'optimization_completed_timestamp': None,
			'parameters': {
				'is_upload': False,
				'rt': False
			},
			'links': {
				'view': (
					'http:\/\/www.route4me.com\/api.v4\/'
					'optimization_problem.php?'
					'optimization_problem_id=1EDB78F63556D99336E06A13A34CF139'
					'&api_key=11111111111111111111111111111111&member_id=1'
				)
			}
		})

		assert opt.links['view'] == (
			'http:\/\/www.route4me.com\/api.v4\/'
			'optimization_problem.php?'
			'optimization_problem_id=1EDB78F63556D99336E06A13A34CF139'
			'&api_key=11111111111111111111111111111111&member_id=1'
		)
