.. include:: common.rst

Date, Time and Timezones
========================

Route4Me works worldwide, this means that we know what the **time zone** is.

Handling time zones is a challenge when we want to handle date and time
correctly for any time zone for many ``python`` implementations. For example,
*python 2* can't process the following code
(`an online proof <https://repl.it/KdT6/0>`__), and *python >3.3* --- can:

.. code-block:: python

	import datetime
	print(datetime.datetime.now().timestamp())

On the other hand, ``python3`` will return :class:`float`, but many Unix users
could expect for an **int**, because ``/bin/date`` returns int:

.. code-block:: bash

	date +%s
	# >> 1504267959

Explicit / TZ-Aware datetime
----------------------------

To avoid most problems, this SDK always use tz-aware :class:`~datetime.datetime`
variables. In most cases, :class:`~datetime.datetime` variables are bound to
**UTC** time zone.

Under the hood we use two additional libraries:

* `arrow`_ (in production code);
* `pytz`_ (for testing purposes);

Display local time
------------------

If you want to print *local* time (not UTC), or time in **any other** time zone
(it is the same moment of time, but convenient for people in the other
location), you could use `arrow`_ package to convert date/time presentation:

.. code-block:: python

	from route4me.sdk import ApiClient
	import arrow

	client = ApiClient(YOUR_API_KEY)
	opt = client.optimizations.get(OPTIMIZATION_ID)

	dt = opt.route_datetime  # Now we have DT in UTC
	print(dt.isoformat())
	# >>> '2016-01-01T12:25:42.465805+00:00'

	# move to local:
	loc = arrow.get(dt).to('local').datetime

	print(loc.isoformat())
	# >>> '2016-01-01T11:25:42.465805-01:00'

	# PROFIT!

.. _arrow: https://pypi.org/project/arrow/
.. _pytz: https://pypi.org/project/pytz/
