# -*- coding: utf-8 -*-
import argparse

from route4me import Route4Me


def main(api_key):
    route4me = Route4Me(api_key)

    activity_feed = route4me.activity_feed
    route = route4me.route
    print('Getting Last Route')
    response = route.get_routes(limit=1, offset=0)
    if isinstance(response, dict) and 'errors' in response.keys():
        print('. '.join(response['errors']))
    else:
        route_id = response[0]['route_id']
        print('Route ID: {}'.format(route_id))
        response = activity_feed.get_activity_feed_deleted(
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
    parser = argparse.ArgumentParser(description='Get Deleted Destination Activities')
    parser.add_argument('--api_key', dest='api_key', help='Route4Me API KEY',
                        type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
