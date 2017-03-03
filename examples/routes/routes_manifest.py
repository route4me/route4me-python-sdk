from route4me import Route4Me
from route4me.constants import (
    ROUTE_PATH_OUTPUT,
)

KEY = "11111111111111111111111111111111"


def main():
    route4me = Route4Me(KEY)
    route = route4me.route
    response = route.get_routes(limit=10, Offset=5)
    if hasattr(response, 'errors'):
        print('. '.join(response.errors))
    else:
        params = {
            'route_id': response[0].route_id,
            'directions': 1,
            'route_path_output': ROUTE_PATH_OUTPUT.POINTS,
            'device_tracking_history': 1,
            'limit': 10,
            'offset': 5,
        }
        response = route.get_route(**params)
        print("Optimization Problem id: {}".format(
            response.optimization_problem_id
        ))
        print("Trip distance: {}".format(response.trip_distance))
        print("Miles per Gallon: {}".format(response.mpg))
        for i, direction in enumerate(response.directions):
            print('Address #{}'.format(i))
            print('Start Location: {}'.format(
                direction.location.start_location
            ))
            print('End Location: {}'.format(direction.location.end_location))
            print('Distance: {}'.format(direction.location.segment_distance))
            print('Time: {}'.format(direction.location.time))
            print('===>Steps')
            for j, step in enumerate(direction.steps):
                print('\tstep #{}'.format(j))
                print('\tDirections: {}'.format(step.directions))
                print('\tDuration: {} sec'.format(step.duration_sec))
                print('\tCompass Direction: {}'.format(step.compass_direction))


if __name__ == '__main__':
    main()
