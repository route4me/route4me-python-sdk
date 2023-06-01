# -*- coding: utf-8 -*-


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
            "store_number": None,
            "store_name": None,
            "address": None,
            "home_city": None,
            "state": None,
            "zip": None,
            "phone": None,
            "lat": None,
            "lng": None
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
        self.group = None

    def to_dict(self):
        result = {}
        for key, value in self.__dict__.items():
            if isinstance(value, dict):
                if all(v is None for v in value.values()):
                    continue
            elif isinstance(value, list):
                if all((isinstance(i, str) and not i) or (isinstance(i, dict) and all(v is None for v in i.values())) for i in value):
                    continue
            if value:
                result[key] = value
        return result
