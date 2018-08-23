# -*- coding: utf-8 -*-

# codebeat:disable[SIMILARITY]
from route4me import Route4Me

API_KEY = "11111111111111111111111111111111"


def main():
    route4me = Route4Me(API_KEY)
    activity_feed = route4me.activity_feed
    response = activity_feed.get_activities_feed(limit=10, offset=0)
    if isinstance(response, dict) and 'errors' in response.keys():
        print('. '.join(response['errors']))
    else:
        print('Total Found: {}'.format(response['total']))
        for i, activity in enumerate(response['results']):
            print('Activity #{}'.format(i + 1))
            print('\tActivity ID: {}'.format(activity['activity_id']))
            print('\tActivity Message: {}'.format(activity['activity_message']))
            print('\tActivity Type: {}'.format(activity['activity_type']))
            print('\tRoute ID: {}'.format(activity['route_id']))


if __name__ == '__main__':
    main()
# codebeat:enable[SIMILARITY]
