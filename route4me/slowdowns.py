# -*- coding: utf-8 -*-

class Slowdowns():
    """
    Slowdowns Management
    """

    def __init__(self, service_time, travel_time):
        self.validate(service_time, travel_time)
        self.service_time = service_time
        self.travel_time = travel_time

    def validate(self, service_time, travel_time):
        if not isinstance(service_time, int) or service_time < 0 or service_time > 50:
            raise ValueError("Service time must be an integer between 0 and 50")

        if not isinstance(travel_time, int) or travel_time < 0 or travel_time > 50:
            raise ValueError("Travel time must be an integer between 0 and 50")

    def to_dict(self):
        return {
            'service_time': self.service_time,
            'travel_time': self.travel_time
        }
