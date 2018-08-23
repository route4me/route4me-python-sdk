# -*- coding: utf-8 -*-

# codebeat:disable[SIMILARITY]
from route4me import Route4Me

API_KEY = "11111111111111111111111111111111"


def main():
    route4me = Route4Me(API_KEY)
    activity_feed = route4me.activity_feed
    route = route4me.route
    print('Getting Last Route')
    response = route.get_routes(limit=1, offset=0)
    if isinstance(response, dict) and 'errors' in response.keys():
        print('. '.join(response['errors']))
    else:
        route_id = response[0]['route_id']
        print('Route ID: {}'.format(route_id))
        response = activity_feed.get_activity_feed_inserted(
            route_id=route_id
        )
        if isinstance(response, dict) and 'errors' in response.keys():
            print('. '.join(response['errors']))
        else:
            print('Total affected: {}'.format(response['total']))
            for i, activity in enumerate(response['results']):
                print('Activity #{}'.format(i + 1))
                print('\tActivity ID: {}'.format(activity['activity_id']))
                print('\tActivity Type: {}'.format(activity['activity_type']))


if __name__ == '__main__':
    main()
# codebeat:enable[SIMILARITY]
