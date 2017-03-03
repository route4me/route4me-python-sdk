import unittest

from tests.base import Route4MeAPITestSuite


class Route4MeRoutesTests(Route4MeAPITestSuite):
    """
    Route4Me Route Tests
    """

    def test_get_routes(self):
        route = self.route4me.route
        response = route.get_routes(limit=10, offset=5)
        if hasattr(response, 'errors'):
            print('. '.join(response.get('errors')))
        else:
            self.assertTrue(len(response) > 0)
            route_id = response[0].get('route_id', False)
            self.assertTrue(route_id)
            response = route.get_route(route_id=route_id)
            self.assertEqual(response.get('route_id'),
                             route_id)


if __name__ == '__main__':
    unittest.main()
