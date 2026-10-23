"""Small helpers: JSON-to-object decoding, dictionary cleaning and datetime checks."""

import json
from collections import namedtuple
from datetime import datetime


def _json_object_hook(d):
    """Turn one decoded JSON object into a namedtuple.

    Keys that start with a digit get a ``d_`` prefix, so that they are valid
    field names.

    :param d: the decoded JSON object.
    :return: a namedtuple with one field per key.
    """
    keys = []
    for k in d.keys():
        if k[0].isdigit():
            k = f"d_{k}"
        keys.append(k)

    return namedtuple("X", keys)(*d.values())


def json2obj(data):
    """Decode a JSON document into namedtuples instead of dicts.

    :param data: the JSON text.
    :return: the decoded document, with every JSON object as a namedtuple
        whose fields are the object's keys.
    """
    return json.loads(data, object_hook=_json_object_hook)


def clean_dict(data):
    """Remove ``None`` values and empty containers, recursively.

    Dicts and lists are cleaned item by item, and a container left empty is
    removed from its parent. Empty strings inside lists are kept. Any other
    value is returned as is.

    :param data: a dict, a list, or a plain value.
    :return: a cleaned copy of ``data``, or ``None`` when nothing is left.
    """
    if isinstance(data, list):
        cleaned_list = []
        for i in data:
            cleaned_item = clean_dict(i)
            # Append non-None items except empty strings
            if cleaned_item or cleaned_item == "":
                cleaned_list.append(cleaned_item)
        return cleaned_list if cleaned_list else None
    if isinstance(data, dict):
        cleaned_dict = {}
        for k, v in data.items():
            cleaned_v = clean_dict(v)
            # Append non-None key-value pairs
            if cleaned_v:
                cleaned_dict[k] = cleaned_v
        return cleaned_dict if cleaned_dict else None
    # For non-container type, return as is
    return data


def is_valid_datetime(s, date_format="%Y-%m-%d %H:%M:%S"):
    """Check whether a value is a date-time in the given format.

    :param s: the value to check; converted with ``str()``.
    :param date_format: a :meth:`datetime.strptime <datetime.datetime.strptime>`
        format. The default is ``YYYY-MM-DD HH:MM:SS``.
    :return: ``True`` if the value matches the format, ``False`` otherwise.
    """
    try:
        datetime.strptime(str(s), date_format)
        return True
    except ValueError:
        return False
