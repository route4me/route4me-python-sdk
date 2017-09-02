# -*- coding: utf-8 -*-


class PagedList(list):
	"""
	Enumerable structure for array-like responses of the Route4Me API.

	Several endpoints of Route4Me API return enumerable responses, which
	contains meta-information about paging (fields like ``total``, ``limit``,
	``offset``). This class allows enumerating requested data along with
	mentioned meta-data fields.
	"""
	def __init__(self, total=None, limit=None, offset=None, items=None):
		_i = tuple() if items is None else items
		super(PagedList, self).__init__(_i)

		self._r4m_total = total
		self._r4m_limit = limit
		self._r4m_offset = offset

	@property
	def total(self):
		"""
		Total results count (taken from API response)

		:getter: Results count, when available
		:rtype: int
		"""
		return self._r4m_total

	@property
	def limit(self):
		"""
		Limit used during endpoint access

		:getter: Value of ``limit`` parameter if it was used in query
		:rtype: int
		"""
		return self._r4m_limit

	@property
	def offset(self):
		"""
		Offset used during endpoint access

		:getter: Value of ``offset`` parameter if it was used in query
		:rtype: int
		"""
		return self._r4m_offset
