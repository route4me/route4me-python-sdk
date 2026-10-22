"""Helpers that build the query and check the body of one request."""

from .exceptions import ParamValueException


def compact(**values):
    """Return the keywords whose value is not ``None``, as a new dict.

    Each call builds its own dict, so the query of one call can never leak
    into the next one (bug #36 came from storing per-call values on
    ``self.params``).

    >>> compact(page=2, per_page=None)
    {'page': 2}

    :param values: query parameter names mapped to values; ``None`` means
        the parameter was not given.
    :return: the parameters that were given.
    """
    return {name: value for name, value in values.items() if value is not None}


def require(fields, required):
    """Check that a request body has every required field.

    :param fields: the body fields given, e.g. a method's ``**fields``.
    :param required: the names that must be present.
    :raise ParamValueException: naming the missing fields.
    """
    missing = [name for name in required if name not in fields]
    if missing:
        raise ParamValueException(", ".join(missing), "Missing required params")
