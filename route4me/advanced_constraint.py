# -*- coding: utf-8 -*-


class AdvancedConstraint(object):

    max_cargo_volume = None
    max_capacity = None
    members_count = 10
    available_time_windows = []
    tags = []
    route4me_members_id = []
    depot_address = []
    location_sequence_pattern = []

    def __init__(self):
        pass

    def to_dict(self):
        return self.__dict__
