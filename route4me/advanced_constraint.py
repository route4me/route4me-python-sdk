# -*- coding: utf-8 -*-

from .utils import clean_dict


class AdvancedConstraint(object):

    def __init__(self):
        self.max_cargo_weight = None
        self.max_cargo_volume = None
        self.max_capacity = None
        self.members_count = 10
        self.vehicles_id = []
        self.available_time_windows = []
        self.tags = []
        self.route4me_members_id = []
        self.depot_address = {
            "alias": None,
            "address": None,
            "lat": None,
            "lng": None,
        }
        self.location_sequence_pattern = [
            "",
            {
                "alias": None,
                "address": None,
                "lat": None,
                "lng": None,
            }
        ]
        self.location_sequence_pattern = [
            "",
            {
                "alias": None,
                "address": None,
                "lat": None,
                "lng": None,
            }
        ]
        self.group = None

    def to_dict(self):
        return clean_dict(self.__dict__)
