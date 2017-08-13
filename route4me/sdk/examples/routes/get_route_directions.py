# codebeat:disable[BLOCK_NESTING, ABC]
from route4me import Route4Me

KEY = "11111111111111111111111111111111"


def main():
    r4m = Route4Me(KEY)
    route = r4m.route
    response = route.get_routes(limit=10, Offset=5)
    if hasattr(response, 'errors'):
        print('. '.join(response.errors))
    else:
        response = route.get_route(route_id=response[0].route_id)
        if hasattr(response, 'errors'):
            print('. '.join(response.errors))
        else:
            print('Route ID: {}'.format(response.route_id))
            data = {
                "directions": 1,
                "route_id": response.route_id
            }
            response = route.get_route_directions(**data)
            print('Optimization Problem ID: {}'.format(
                response.optimization_problem_id
            ))
            print('Route ID: {}'.format(response.route_id))
            for i, direction in enumerate(response.directions):
                print('Direction #{}'.format(i))
                print('\tLocation')
                print('\t\tTime: {}'.format(direction.location.time))
                print('\t\tName: {}'.format(direction.location.name))
                print('\t\tStart Location: {}'.format(
                    direction.location.start_location
                ))
                print('\t\tEnd Location: {}'.format(
                    direction.location.end_location
                ))
                print('\tSteps')
                for step in direction.steps:
                    print('\t\tDirections: {}'.format(step.directions))
                    print('\t\tDirection: {}'.format(step.direction))
                    print('\t\tDistance: {}'.format(step.distance))
                    print('\t\tDistance unit: {}'.format(step.distance_unit))
                    print('\t\tManeuver Type: {}'.format(step.maneuverType))
                    print('\t\tCompass Direction: {}'.format(
                        step.compass_direction
                    ))
                    print('\t\tDuration sec: {}'.format(step.duration_sec))
                    print('\t\tManeuver Point')
                    print('\t\t\tLat: {}'.format(step.maneuverPoint.lat))
                    print('\t\t\tLng: {}'.format(step.maneuverPoint.lng))


if __name__ == '__main__':
    main()
# codebeat:enable[BLOCK_NESTING, ABC]
