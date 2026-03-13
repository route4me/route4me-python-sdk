# -*- coding: utf-8 -*-

from .exceptions import ParamValueException


class ValidatedField:
    """
    Descriptor that replaces boilerplate setter methods in Base.
    ``obj.field_name(value)`` validates and copies to params or data.
    """

    def __init__(self, name, vtype, target, error_msg, *,
                 enum_cls=None, valid_values=None, valid_range=None):
        self.name = name
        self.vtype = vtype
        self.target = target
        self.error_msg = error_msg
        self.enum_cls = enum_cls
        self.valid_values = valid_values
        self.valid_range = valid_range

    def __set_name__(self, owner, attr_name):
        self.attr_name = attr_name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        def setter(value):
            self._validate_and_set(obj, value)
        return setter

    def _validate_and_set(self, obj, value):
        vtype = self.vtype
        if vtype is str:
            if not isinstance(value, str):
                raise ParamValueException(self.name, self.error_msg)
        elif vtype is int:
            if not isinstance(value, int):
                raise ParamValueException(self.name, self.error_msg)
        elif vtype == 'numeric':
            if not isinstance(value, (int, float)):
                raise ParamValueException(self.name, self.error_msg)
        elif vtype == 'float_strict':
            if not isinstance(value, float):
                raise ParamValueException(self.name, self.error_msg)
        elif vtype == 'boolish':
            if not (isinstance(value, int) and 0 <= value <= 1):
                raise ParamValueException(self.name, self.error_msg)
        elif vtype == 'enum':
            if value not in self.enum_cls.reverse_mapping.keys():
                raise ParamValueException(self.name, self.error_msg)
        elif vtype == 'oneof':
            if value not in self.valid_values:
                raise ParamValueException(self.name, self.error_msg)
        elif vtype == 'range':
            if not (self.valid_range[0] <= value <= self.valid_range[1]):
                raise ParamValueException(self.name, self.error_msg)

        copy_fn = getattr(obj, '_copy_%s' % self.target)
        copy_fn({self.name: value})
