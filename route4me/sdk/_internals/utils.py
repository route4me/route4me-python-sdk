# -*- coding: utf-8 -*-

import pydash


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
			v = pydash.get(self, path)
			return enumtype(v)

		def _set(self, value):
			if isinstance(value, enumtype):
				value = value.value
			value = fn(self, value)
			pydash.set_(self, path, value)

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


def dict_property(path, anytype):
	def decorator(fn):

		def _get(self):
			v = pydash.get(self, path)
			return anytype(v)

		def _set(self, value):
			value = fn(self, value)
			pydash.set_(self, path, value)

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
