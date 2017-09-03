# -*- coding: utf-8 -*-

import datetime

import arrow


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
