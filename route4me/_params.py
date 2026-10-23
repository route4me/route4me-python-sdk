"""Helpers that build the query and check the body of one request.

:func:`compact` drops the keywords a caller did not give, :func:`require`
checks the body fields the API requires, and :func:`nested_query` encodes list
and dict query values the way API V5 reads them.
"""

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


def nested_query(params):
    """Flatten the dict and list values of a query into bracketed keys.

    API V5 runs on PHP, which reads an array or an object from the query string
    only when the key carries brackets: ``ids[]=1&ids[]=2`` is a list, but
    ``ids=1&ids=2`` keeps only the last value. ``requests`` sends a list as the
    repeated plain key and cannot send a dict or a nested list at all, so the
    client passes every V5 query through this function.

    A dict becomes one ``name[key]`` entry per item, and a list of plain values
    becomes ``name[]``, which ``requests`` repeats once per value. A list that
    holds dicts or lists is indexed, ``name[0][key]``. Other values are kept
    as they are.

    >>> nested_query({"page": 1, "filters": {"status": [1, 2]}})
    {'page': 1, 'filters[status][]': [1, 2]}
    >>> nested_query({"order_by": [{"name": "asc"}]})
    {'order_by[0][name]': 'asc'}

    :param params: the query, name to value.
    :return: a new dict whose values are plain values or lists of them.
    """
    flat = {}
    for name, value in params.items():
        _flatten_into(flat, str(name), value)
    return flat


def _flatten_into(flat, key, value):
    """Add one query value to ``flat``, flattening it under ``key``.

    :param flat: the dict being built.
    :param key: the key of the value, already bracketed for nested values.
    :param value: the value to add.
    """
    if isinstance(value, dict):
        for name, item in value.items():
            _flatten_into(flat, f"{key}[{name}]", item)
    elif isinstance(value, (list, tuple)):
        if any(isinstance(item, (dict, list, tuple)) for item in value):
            for index, item in enumerate(value):
                _flatten_into(flat, f"{key}[{index}]", item)
        else:
            flat[f"{key}[]"] = list(value)
    else:
        flat[key] = value
