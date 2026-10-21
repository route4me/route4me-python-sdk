"""The :class:`Slowdowns` model for an optimization's ``slowdowns`` parameter."""


class Slowdowns:
    """Percentages by which service and travel times are increased.

    :param service_time: service-time slowdown, an integer percentage from 0
        to 50.
    :param travel_time: travel-time slowdown, an integer percentage from 0 to
        50.
    :raise ValueError: when either value is not an integer from 0 to 50.
    """

    def __init__(self, service_time, travel_time):
        self.validate(service_time, travel_time)
        self.service_time = service_time
        self.travel_time = travel_time

    def validate(self, service_time, travel_time):
        """Check both slowdown values.

        :param service_time: service-time slowdown to check.
        :param travel_time: travel-time slowdown to check.
        :raise ValueError: when either value is not an integer from 0 to 50.
        """
        if not isinstance(service_time, int) or service_time < 0 or service_time > 50:
            raise ValueError("Service time must be an integer between 0 and 50")

        if not isinstance(travel_time, int) or travel_time < 0 or travel_time > 50:
            raise ValueError("Travel time must be an integer between 0 and 50")

    def to_dict(self):
        """Return the slowdowns as a dict for the request body.

        :return: ``{"service_time": ..., "travel_time": ...}``.
        """
        return {"service_time": self.service_time, "travel_time": self.travel_time}
