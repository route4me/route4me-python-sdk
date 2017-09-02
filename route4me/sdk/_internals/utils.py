# -*- coding: utf-8 -*-

import six
import datetime
import logging

import pydash
import arrow

log = logging.getLogger(__name__)


def _handle_auto_doc_for_property(doc, typename):
	if doc is None:
		doc = '<AUTO>'

	if '<AUTO>' in doc:
		subst = (
			':getter: Get\n'
			'{pref}:setter: Set\n'
			'{pref}:rtype: {typename}'
		).format(
			typename=typename,
			pref='\t\t',
		)
		doc = doc.replace('<AUTO>', subst)

	return doc


def dict_enum_property(path, enumtype):
	def decorator(fn):

		def _get(self):
			v = pydash.get(self.raw, path)

			if v is None:
				return None

			return enumtype(v)

		def _set(self, value):
			if isinstance(value, enumtype):
				value = value.value
			value = fn(self, value)
			pydash.set_(self.raw, path, value)

			return enumtype(value)

		doc = _handle_auto_doc_for_property(
			fn.__doc__,
			'~{mod}.{nm}'.format(
				mod=enumtype.__module__,
				nm=enumtype.__name__,
			)
		)

		p = property(_get, _set, None, doc)
		return p
	return decorator


# TODO: test over unicode in python 2
def dict_property(path, anytype):
	"""
	Creates new strict-typed PROPERTY for classes inherited from :class:`dict`
	"""

	def decorator_str(fn):

		def _get(self):
			v = pydash.get(self.raw, path)

			if v is None:
				return None

			return six.text_type(v)

		def _set(self, value):
			v = six.text_type(value)
			v = fn(self, v)
			pydash.set_(self.raw, path, v)

			return v

		doc = fn.__doc__

		typename = type(six.text_type('')).__name__

		doc = _handle_auto_doc_for_property(
			fn.__doc__,
			typename
		)

		p = property(_get, _set, None, doc)

		return p

	def decorator_other(fn):

		def _get(self):
			v = pydash.get(self.raw, path)

			if v is None:
				return None

			return anytype(v)

		def _set(self, value):
			v = fn(self, value)
			pydash.set_(self.raw, path, v)

			return v

		doc = fn.__doc__

		if doc is None:
			doc = '<AUTO>'

		typename = anytype.__name__

		doc = _handle_auto_doc_for_property(
			fn.__doc__,
			typename
		)

		p = property(_get, _set, None, doc)

		return p

	if anytype == str:
		return decorator_str

	return decorator_other


def unix_timestamp_today(tz=None):
	"""
	Returns unix timestamp for TODAY (00:00) in ``tz`` timezone (UTC by default)

	:param tz: Timezone, defaults to None (UTC)
	:type tz: datetime.tzinfo, optional
	:returns: Unix-timestamp (seconds) for today
	:rtype: int
	"""
	return arrow.get(tz).floor('day').timestamp


def timestamp_and_seconds2datetime(ts, sec=0):

	if ts is None:
		return None
	if sec is None:
		sec = 0

	dd = arrow.get(int(ts) + int(sec))
	return dd.datetime


def datetime2timestamp_and_seconds(dt):
	if not isinstance(dt, datetime.datetime):
		raise TypeError('dt', 'datetime.datetime expected!')

	adt = arrow.get(dt)

	ts = adt.floor('day').timestamp
	sec = adt.timestamp - ts
	return ts, sec


def add_limit_offset_to_query_string(limit, offset, qs):
	if limit is not None:
		qs['limit'] = limit

	if offset is not None:
		qs['offset'] = offset

	return qs
