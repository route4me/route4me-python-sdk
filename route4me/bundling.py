from dataclasses import dataclass, field

from .constants import enum

BUNDLING_MODE = enum(BY_ADDRESS=1, BY_COORDINATES=2, BY_STATIC_FIELD=3, BY_CUSTOM_DATA=4)

BUNDLING_MERGE_MODE = enum(KEEP_SEPARATED=1, MERGE_INTO_SINGLE=2)

BUNDLING_FIRST_ITEM_MODE = enum(KEEP_ORIGINAL_SERVICE_TIME=1, USE_CUSTOM_SERVICE_TIME=2)

BUNDLING_ADDITIONAL_ITEM_MODE = enum(KEEP_ORIGINAL_SERVICE_TIME=1, USE_CUSTOM_SERVICE_TIME=2, DO_NOT_ADD_SERVICE_TIME=3)


class ServiceTimeRules(dict):
    first_item_mode = None
    first_item_mode_params = []
    additional_items_mode = None
    additional_items_mode_params = []

    def __init__(self):
        pass

    def to_dict(self):
        return self.__dict__


@dataclass
class Bundling:
    mode: int = BUNDLING_MODE.BY_ADDRESS
    merge_mode: int = BUNDLING_MERGE_MODE.KEEP_SEPARATED
    mode_params: list = field(default_factory=list)
    service_time_rules: ServiceTimeRules = field(default_factory=ServiceTimeRules)

    def to_dict(self):
        return self.__dict__
