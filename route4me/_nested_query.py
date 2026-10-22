"""Encode nested query parameters with bracketed keys.

API V5 runs on PHP, which reads an array or an object from the query string
only when the key carries brackets: ``ids[]=1&ids[]=2`` is a list, but
``ids=1&ids=2`` keeps only the last value. ``requests`` sends a list as the
repeated plain key and cannot send a dict at all, so the V5 resources pass
their query through :func:`nested_query` first.
"""


def nested_query(params):
    """Flatten the dict and list values of a query into bracketed keys.

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
