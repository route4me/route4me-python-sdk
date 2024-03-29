# -*- coding: utf-8 -*-

import json
from collections import namedtuple


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
            # Append non-None items
            if cleaned_item not in [None, ""]:
                cleaned_list.append(cleaned_item)
        return cleaned_list if cleaned_list else None
    elif isinstance(data, dict):
        cleaned_dict = {}
        for k, v in data.items():
            cleaned_v = clean_dict(v)
            # Append non-None key-value pairs
            if cleaned_v not in [None, ""]:
                cleaned_dict[k] = cleaned_v
        return cleaned_dict if cleaned_dict else None
    else:
        # For non-container type, return as is
        return data
