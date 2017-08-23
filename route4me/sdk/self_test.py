# -*- coding: utf-8 -*-

import mock


class MockerResourceWithNetworkClient:

	resource_module = None
	client = None

	@classmethod
	def setup_class(cls):

		# there are several similar modules-resources.
		# all we need to test them -- mock NetworkClient, to prevent
		# network access.
		# Let's do it with mock.patch.object
		#
		# Mocked client will be accessible in tests as `cls.client`

		cls.client = mock.MagicMock()

		cls.patcher_client = mock.patch.object(cls.resource_module, 'NetworkClient')
		mock_client = cls.patcher_client.start()
		mock_client.return_value = cls.client

	@classmethod
	def teardown_class(cls):
		"""Teardown test environment for the entire class
		"""
		cls.patcher_client.stop()
