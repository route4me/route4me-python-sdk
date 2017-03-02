from collections import namedtuple
import json


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


def check_string_type(obj):
    """
    Check if an object is string type
    :param obj:
    :return:
    """
    try:
        return isinstance(obj, basestring)
    except NameError:
        return isinstance(obj, str)
