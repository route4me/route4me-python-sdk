from .exceptions import ParamValueException

#: How each ``vtype`` validates a value. An unknown ``vtype`` accepts anything.
_CHECKS = {
    str: lambda field, value: isinstance(value, str),
    int: lambda field, value: isinstance(value, int),
    "numeric": lambda field, value: isinstance(value, (int, float)),
    "float_strict": lambda field, value: isinstance(value, float),
    "boolish": lambda field, value: isinstance(value, int) and 0 <= value <= 1,
    "enum": lambda field, value: value in field.enum_cls.reverse_mapping,
    "oneof": lambda field, value: value in field.valid_values,
    "range": lambda field, value: field.valid_range[0] <= value <= field.valid_range[1],
}


class ValidatedField:
    """
    Descriptor that replaces boilerplate setter methods in Base.
    ``obj.field_name(value)`` validates and copies to params or data.
    """

    def __init__(self, name, vtype, target, error_msg, *, enum_cls=None, valid_values=None, valid_range=None):
        self.name = name
        self.vtype = vtype
        self.target = target
        self.error_msg = error_msg
        self.enum_cls = enum_cls
        self.valid_values = valid_values
        self.valid_range = valid_range
        self.attr_name = None

    def __set_name__(self, owner, attr_name):
        self.attr_name = attr_name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self

        def setter(value):
            self._validate_and_set(obj, value)

        return setter

    def _validate_and_set(self, obj, value):
        check = _CHECKS.get(self.vtype)
        if check is not None and not check(self, value):
            raise ParamValueException(self.name, self.error_msg)
        getattr(obj, f"_copy_{self.target}")({self.name: value})
