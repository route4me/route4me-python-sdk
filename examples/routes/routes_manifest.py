from route4me import Route4Me
from route4me.constants import *

KEY = "11111111111111111111111111111111"


def main():
    route4me = Route4Me(KEY)
    route = route4me.route
    response = route.get_routes(limit=10, Offset=5)
    if hasattr(response, 'errors'):
        print '. '.join(response.errors)
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
        print "Optimization Problem id: %s" % response.optimization_problem_id
        print "Trip distance %f" % response.trip_distance
        print "Miles per Galon %f" % response.mpg
        for i, direction in enumerate(response.directions):
            print 'Address #%d' % i
            print 'Start Location: %s' % direction.location.start_location
            print 'End Location: %s' % direction.location.end_location
            print 'Distance: %s' % direction.location.segment_distance
            print 'Time: %s' % direction.location.time
            print '===>Steps'
            for j, step in enumerate(direction.steps):
                print '\tstep #%d' % j
                print '\tDirections: %s' % step.directions
                print '\tDuration: %d sec' % step.duration_sec
                print '\tCompass Direction: %s' % step.compass_direction

if __name__ == '__main__':
    main()
