# -*- coding: utf-8 -*-

import pytest
import datetime

import pytz

from .utils import timestamp_and_seconds2datetime
from .utils import datetime2timestamp_and_seconds


class Test_timestamp_and_seconds2datetime(object):

	@pytest.mark.parametrize('d, t', [
		(None, 11),
		(None, None),
	])
	def test_when_none(self, d, t):
		act = timestamp_and_seconds2datetime(d, t)

		assert act is None

	@pytest.mark.parametrize('d, t, exp', [
		# 1400111222
		# 2014-05-14T23:47:02+00:00
		# (from https://www.unixtimestamp.com/index.php)
		(1400111222, None, datetime.datetime(2014, 5, 14, 23, 47, 2, tzinfo=pytz.utc)),
		(1400111222, 11, datetime.datetime(2014, 5, 14, 23, 47, 13, tzinfo=pytz.utc)),

		# 1504137600 is equivalent to:
		# 2017-08-31T00:00:00+00:00 in ISO 8601
		# (from https://www.unixtimestamp.com/index.php)
		(1504137600, 0, datetime.datetime(2017, 8, 31, 0, 0, 0, tzinfo=pytz.utc)),
		(1504137600, 16281, datetime.datetime(2017, 8, 31, 4, 31, 21, tzinfo=pytz.utc)),
	])
	def test_normal_conversion_in_utc(self, d, t, exp):
		act = timestamp_and_seconds2datetime(d, t)

		assert act == exp

	@pytest.mark.parametrize('d, t, exp', [
		# 1504222593
		# 2017-08-31T23:36:33+00:00 in ISO 8601
		(1504222593, 0, datetime.datetime(2017, 8, 31, 23, 36, 33, tzinfo=pytz.utc)),
		(1504222593, 11, datetime.datetime(2017, 8, 31, 23, 36, 44, tzinfo=pytz.utc)),  # UTC!!
	])
	def test_should_not_drop_TIME_in_from_first_argument(self, d, t, exp):
		act = timestamp_and_seconds2datetime(d, t)

		assert act == exp


class Test_datetime2timestamp_and_seconds(object):

	TIMEZONE_0300 = pytz.FixedOffset(180)

	@pytest.mark.parametrize('dt', [
		(None),
		(11),
		('asdf'),
		(True),
		(4.5),
		(0),
	])
	def test_raise_on_wrong_type(self, dt):
		with pytest.raises(TypeError) as exc_info:
			datetime2timestamp_and_seconds(dt)

		exc = exc_info.value
		assert 'datetime' in str(exc)
		assert 'dt' in str(exc)

	@pytest.mark.parametrize('dt, exp_ts, exp_sec', [
		(datetime.datetime(2014, 5, 14, 0, 0, 11, tzinfo=pytz.utc), 1400025600, 11),

		# 1504137600 is equivalent to:
		# 2017-08-31T00:00:00+00:00 in ISO 8601
		# (from https://www.unixtimestamp.com/index.php)
		(datetime.datetime(2017, 8, 31, 0, 0, 0, tzinfo=pytz.utc), 1504137600, 0),
		(datetime.datetime(2017, 8, 31, 4, 31, 21, tzinfo=pytz.utc), 1504137600, 16281),
	])
	def test_normal_conversion_in_utc(self, dt, exp_ts, exp_sec):
		act_ts, act_sec = datetime2timestamp_and_seconds(dt)

		assert act_ts == exp_ts
		assert act_sec == exp_sec

	@pytest.mark.parametrize('dt, exp_ts, exp_sec', [
		(datetime.datetime(2014, 5, 14, 0, 0, 11, tzinfo=TIMEZONE_0300), 1400014800, 11),

		# 1504137600 is equivalent to:
		# 2017-08-31T00:00:00+00:00 in ISO 8601
		# (from https://www.unixtimestamp.com/index.php)
		(datetime.datetime(2017, 8, 31, 0, 0, 0, tzinfo=TIMEZONE_0300), 1504126800, 0),
		(datetime.datetime(2017, 8, 31, 4, 31, 21, tzinfo=TIMEZONE_0300), 1504126800, 16281),
	])
	def test_normal_conversion_in_0300(self, dt, exp_ts, exp_sec):
		act_ts, act_sec = datetime2timestamp_and_seconds(dt)

		assert act_ts == exp_ts
		assert act_sec == exp_sec
