# -*- coding: utf-8 -*-

import six

"""
Type-conversion helpers

This module contains several classes and functions for parsing and converting
types.

Most functions are designed to work like default functions: :class:`int`
:class:`bool` --- take at least one parameter and return well-typed value.
"""


def str2bool(strvalue, default=None):
	"""
	Converts string value to :class:`bool`. Can parse human-readable values,
	like ``'yes'`` and ``'off'``.

	If value is not recognized -- the value of the :paramref:`~str2bool.default`
	argument will be returned.

	.. note::

		:func:`str2bool` is not an extension of default :class:`bool`. For
		example, it doesn't recognize integer ``2`` (or any other number) as
		:data:`True` value.

	:param strvalue: Value to parse
	:type strvalue: str
	:param default:  Default value, defaults to :data:`None`
	:type default: *
	:returns: Parsed boolean value or :paramref:`~str2bool.default` \
	(if defined). Not a bool value will be returned **only** if value was not \
	recognized.
	:rtype: bool or *

	"""
	if strvalue is None:
		return default

	rl = str(strvalue).lower()
	if rl in ['true', '1', 't', 'y', 'yes', 'on']:
		return True
	if rl in ['false', '0', 'f', 'n', 'no', 'off']:
		return False

	return default


def bool201(boolvalue):
	"""
	Converts :class:`bool` value to string: ``u'0'`` or ``u'1'`` --- a returned
	value is in unicode.

	:param boolvalue: Value to convert
	:type boolvalue: bool
	:returns: String ``'0'`` or ``'1'``
	:rtype: str
	:raises TypeError: if not a bool argument was passed
	"""
	if not isinstance(boolvalue, bool):
		raise TypeError('bool expected')

	if boolvalue:
		return six.text_type('1')
	return six.text_type('0')
