# -*- coding: utf-8 -*-

import json
from collections import namedtuple
from datetime import datetime


def _json_object_hook(d):
    """
    JSON to object helper
    :param d: data
    :return: namedtuple
    """
    keys = []
    for k in d.keys():
        if k[0].isdigit():
            k = 'd_{}'.format(k)
        keys.append(k)

    return namedtuple('X', keys)(*d.values())


def json2obj(data):
    """
    Parse JSON to object
    :param data: JSON data
    :return: object
    """
    return json.loads(data, object_hook=_json_object_hook)


def clean_dict(data):
    """
    Clean dictionary values
    :param data: input dictionary
    :return: cleaned dictionary
    """
    if isinstance(data, list):
        cleaned_list = []
        for i in data:
            cleaned_item = clean_dict(i)
            # Append non-None items except empty strings
            if cleaned_item or cleaned_item == "":
                cleaned_list.append(cleaned_item)
        return cleaned_list if cleaned_list else None
    elif isinstance(data, dict):
        cleaned_dict = {}
        for k, v in data.items():
            cleaned_v = clean_dict(v)
            # Append non-None key-value pairs
            if cleaned_v:
                cleaned_dict[k] = cleaned_v
        return cleaned_dict if cleaned_dict else None
    else:
        # For non-container type, return as is
        return data


def is_valid_datetime(s):
    """
    Checks if the given datetime string is in 'YYYY-MM-DD HH:MM:SS' format.
    :param s: The datetime string to validate.
    :return: True if the datetime string is valid, False otherwise.
    """
    try:
        datetime.strptime(str(s), '%Y-%m-%d %H:%M:%S')
        return True
    except ValueError:
        return False
