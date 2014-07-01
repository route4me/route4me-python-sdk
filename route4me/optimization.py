from base import Base


class Optimization(Base):
    """
        An Optimization Problem is a collection of addresses that need to be
        visited. This is distinct from a Route, which is a sequence of
        addresses that need to be visited by a single vehicle and a single
        driver in a fixed time period. Solving an Optimization Problem
        results in a number of routes.
    """

    def __init__(self, api):
        """
        Optimization Instance
        :param api:
        :return:
        """
        Base.__init__(self, api)

