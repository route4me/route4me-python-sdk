# -*- coding: utf-8 -*-

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
	def decorator(fn):

		def _get(self):
			v = pydash.get(self.raw, path)

			if v is None:
				return None

			return anytype(v)

		def _set(self, value):
			value = fn(self, value)
			pydash.set_(self.raw, path, value)

			return value

		doc = fn.__doc__

		if doc is None:
			doc = '<AUTO>'

		doc = _handle_auto_doc_for_property(
			fn.__doc__,
			anytype.__name__
		)

		p = property(_get, _set, None, doc)
		return p
	return decorator


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
