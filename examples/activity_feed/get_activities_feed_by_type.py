# -*- coding: utf-8 -*-

# codebeat:disable[SIMILARITY]
import argparse

from route4me import Route4Me

ACTIVITY_TYPE = (
    'delete-destination',
    'insert-destination',
    'mark-destination-departed',
    'mark-destination-visited',
    'member-created',
    'member-deleted',
    'member-modified',
    'move-destination',
    'note-insert',
    'route-delete',
    'route-optimized',
    'route-owner-changed',
    'update-destinations',
    'area-added',
    'area-removed',
    'area-updated',
    'destination-out-sequence',
    'driver-arrived-early',
    'driver-arrived-on-time',
    'driver-arrived-late',
    'geofence-entered',
    'geofence-left',
    'message',
    'local-geofence-entered',
    'local-geofence-left',
    'vehicle-added',
    'vehicle-removed',
    'route-vehicle-changed',
)


def main(api_key):
    route4me = Route4Me(api_key)

    activity_feed = route4me.activity_feed
    for activity_type in ACTIVITY_TYPE:
        response = activity_feed.get_activities_feed_by_type(
            activity_type=activity_type,
            limit=1,
            offset=0
        )
        print(' '.join(activity_type.split('-')).upper())
        if isinstance(response, dict) and 'errors' in response.keys():
            print('. '.join(response['errors']))
        else:
            print('Total Found: {}'.format(response['total']))
            for i, activity in enumerate(response['results']):
                print('Activity #{}'.format(i + 1))
                print('\tActivity ID: {}'.format(activity['activity_id']))
                print('\tActivity Message: {}'.format(
                    activity['activity_message']
                ))
                print('\tActivity Type: {}'.format(activity['activity_type']))
                print('\tRoute ID: {}'.format(activity['route_id']))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Get Activities Feed by Type')
    parser.add_argument('--api_key', dest='api_key', help='Route4Me API KEY',
                        type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)

# codebeat:enable[SIMILARITY]
