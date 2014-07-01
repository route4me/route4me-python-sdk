from collections import namedtuple
import json


def _json_object_hook(d):
    """
    JSON to object helper
    :param d: data
    :return: namedtuple
    """
    return namedtuple('X', d.keys())(*d.values())


def json2obj(data):
    """
    Parse JSON to object
    :param data: JSON data
    :return: object
    """
    return json.loads(data, object_hook=_json_object_hook)