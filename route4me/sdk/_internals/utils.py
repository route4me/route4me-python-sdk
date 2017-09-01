# -*- coding: utf-8 -*-

import six

import pydash
import datetime
import logging


log = logging.getLogger(__name__)


if six.PY2:
	import time

	def get6_timestamp(dt):
		return int(time.mktime(dt.timetuple()))

	def get6_total_seconds(td):
		return td.seconds + td.days * 24 * 3600

else:
	def get6_timestamp(dt):
		return int(dt.timestamp())

	def get6_total_seconds(td):
		return td.total_seconds()


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


def timestamp_and_seconds2datetime(unix_timestamp, seconds):

	d = unix_timestamp
	t = seconds

	if d is None:
		return None
	if t is None:
		return None

	dd = datetime.datetime.utcfromtimestamp(d)
	# lets drop hours/minutes/seconds
	if dd.hour + dd.minute + dd.second > 0:
		log.warn('route date contains TIME info; expected only DATE')

	dd = dd.replace(
		hour=0,
		minute=0,
		second=0,
		microsecond=0
	)

	return dd + datetime.timedelta(seconds=t)


def datetime2timestamp_and_seconds(dt):
	if not isinstance(dt, datetime.datetime):
		raise TypeError('dt', 'datetime.datetime expected!')

	d = dt.replace(
		hour=0,
		minute=0,
		second=0,
		microsecond=0,
	)
	td = dt - d

	ts = get6_timestamp(d)
	sec = get6_total_seconds(td)
	return ts, sec
