"""Validated setters for API parameters, declared as descriptors on :class:`~route4me.base.Base`."""

from .exceptions import ParamValueException

#: How each ``vtype`` validates a value. An unknown ``vtype`` accepts anything.
_CHECKS = {
    str: lambda field, value: isinstance(value, str),
    int: lambda field, value: isinstance(value, int),
    "numeric": lambda field, value: isinstance(value, (int, float)),
    "number": lambda field, value: isinstance(value, (int, float)) and not isinstance(value, bool),
    "boolish": lambda field, value: isinstance(value, int) and 0 <= value <= 1,
    "enum": lambda field, value: value in field.enum_cls.reverse_mapping,
    "oneof": lambda field, value: value in field.valid_values,
    "range": lambda field, value: field.valid_range[0] <= value <= field.valid_range[1],
}


class ValidatedField:
    """Descriptor that turns a class attribute into a validated setter.

    Reading the attribute on an instance returns a function of one value:
    ``obj.field_name(value)`` validates the value and copies it into the query
    parameters or the route parameters of ``obj``.

    :param name: key the value is stored under, usually the attribute name.
    :param vtype: validation kind: ``str``, ``int``, ``"numeric"`` (int or
        float), ``"number"`` (int or float, not bool), ``"boolish"`` (0 or 1),
        ``"enum"``, ``"oneof"`` or ``"range"``. Any other value accepts
        everything.
    :param target: ``"param"`` for the query parameters, ``"data"`` for the
        route parameters.
    :param error_msg: message of the
        :class:`~route4me.exceptions.ParamValueException` raised on an invalid
        value.
    :param enum_cls: for ``"enum"``: a type built by
        :func:`~route4me.constants.enum`; valid values are its member values.
    :param valid_values: for ``"oneof"``: the accepted values.
    :param valid_range: for ``"range"``: inclusive ``(low, high)`` bounds.
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
        """Record the attribute name this field is assigned to.

        :param owner: the class that declares the field.
        :param attr_name: the attribute name.
        """
        self.attr_name = attr_name

    def __get__(self, obj, objtype=None):
        """Return the setter bound to ``obj``, or the field itself on the class.

        :param obj: the instance the attribute is read from, or ``None``.
        :param objtype: the class.
        :return: a function of one value that validates and stores it; this
            field when read on the class.
        """
        if obj is None:
            return self

        def setter(value):
            """Validate ``value`` and store it.

            :param value: the parameter value.
            """
            self._validate_and_set(obj, value)

        return setter

    def _validate_and_set(self, obj, value):
        """Validate ``value`` and copy it into ``obj``'s target dict.

        :param obj: the resource to update.
        :param value: the parameter value.
        :raise ParamValueException: when the value fails validation.
        """
        check = _CHECKS.get(self.vtype)
        if check is not None and not check(self, value):
            raise ParamValueException(self.name, self.error_msg)
        getattr(obj, f"_copy_{self.target}")({self.name: value})
