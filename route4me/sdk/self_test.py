# -*- coding: utf-8 -*-

import mock


class MockerResourceWithNetworkClient(object):

	resource_module = None

	mock_fluent_request_class = None

	@classmethod
	def setup_method(cls, *args, **qw):

		# there are several similar modules-resources.
		# all we need to test them -- mock NetworkClient, to prevent
		# network access.
		# Let's do it with mock.patch.object
		#
		# Mocked client will be accessible in tests as `cls.client`

		# mock FluentRequest
		cls._patcher_fluent_request_class = mock.patch(
			'route4me.sdk._net.FluentRequest'
		)
		cls.mock_fluent_request_class = cls._patcher_fluent_request_class.start()

	@classmethod
	def teardown_method(cls, *args, **qw):
		"""Teardown test environment for the entire class
		"""
		cls._patcher_fluent_request_class.stop()

	def set_response(self, status_code=200, data=None, **qw):

		x = mock.MagicMock()
		x.status_code = status_code
		x.json.return_value = data

		for k in qw:
			x.k = qw[k]

		self.mock_fluent_request_class.return_value.send.return_value = x

	def last_request(self):
		return self.mock_fluent_request_class.return_value
