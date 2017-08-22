# -*- coding: utf-8 -*-

# reimport enums for convenience:
from ..enums import *


class BaseModel(dict):
	pass


class Optimization(BaseModel):
	"""
	Optimization problem (or simple *Optimization*)
	"""

	@property
	def algorithm_type(self):
		"""
		The algorithm type to be used

		:getter: get doc
		:setter: setterd doc
		:rtype: ~route4me.sdk.enums.AlgorithmTypeEnum
		"""
		return self['parameters']['algorithm_type']

	@algorithm_type.setter
	def algorithm_type(self, value):
		old = self['parameters']['algorithm_type']
		self['parameters']['algorithm_type'] = value
		return old
