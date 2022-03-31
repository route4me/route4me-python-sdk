# -*- coding: utf-8 -*-

from .constants import enum

BUNDLING_MODE = enum(BY_ADDRESS=1,
                     BY_COORDINATES=2,
                     BY_STATIC_FIELD=3,
                     BY_CUSTOM_DATA=4)

BUNDLING_MERGE_MODE = enum(KEEP_SEPARATED=1,
                           MERGE_INTO_SINGLE=2)

BUNDLING_FIRST_ITEM_MODE = enum(KEEP_ORIGINAL_SERVICE_TIME=1,
                                USE_CUSTOM_SERVICE_TIME=2)

BUNDLING_ADDITIONAL_ITEM_MODE = enum(KEEP_ORIGINAL_SERVICE_TIME=1,
                                     USE_CUSTOM_SERVICE_TIME=2,
                                     DO_NOT_ADD_SERVICE_TIME=3)


class ServiceTimeRules(dict):

    first_item_mode = None
    first_item_mode_params = []
    additional_items_mode = None
    additional_items_mode_params = []

    def __init__(self):
        pass

    def to_dict(self):
        return self.__dict__


class Bundling(object):

    def __init__(self):
        self.service_time_rules = ServiceTimeRules()
        self.mode = BUNDLING_MODE.BY_ADDRESS
        self.merge_mode = BUNDLING_MERGE_MODE.KEEP_SEPARATED
        self.mode_params = []

    def to_dict(self):
        return self.__dict__
