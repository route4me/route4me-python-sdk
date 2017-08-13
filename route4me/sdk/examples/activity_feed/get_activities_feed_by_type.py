# codebeat:disable[SIMILARITY]
from route4me import Route4Me

KEY = "11111111111111111111111111111111"

ACTYVITY_TYPE = (
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


def main():
    route4me = Route4Me(KEY)
    activity_feed = route4me.activity_feed
    for activity_type in ACTYVITY_TYPE:
        response = activity_feed.get_activities_feed_by_type(
            activity_type=activity_type,
            limit=1,
            offset=0
        )
        print(' '.join(activity_type.split('-')).upper())
        if hasattr(response, 'errors'):
            print('. '.join(response.errors))
        else:
            print('Total Found: {}'.format(response.total))
            for i, activity in enumerate(response.results):
                print('Activity #{}'.format(i + 1))
                print('\tActivity ID: {}'.format(activity.activity_id))
                print('\tActivity Message: {}'.format(
                    activity.activity_message
                ))
                print('\tActivity Type: {}'.format(activity.activity_type))
                print('\tRoute ID: {}'.format(activity.route_id))
                print('\tRoute Name: {}'.format(activity.route_name))


if __name__ == '__main__':
    main()
# codebeat:enable[SIMILARITY]
