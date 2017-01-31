# codebeat:disable[SIMILARITY]
from route4me import Route4Me

KEY = "11111111111111111111111111111111"


def main():
    route4me = Route4Me(KEY)
    activity_feed = route4me.activity_feed
    response = activity_feed.get_activity_feed_deleted(route_id='5C15E83A4BE005BCD1537955D28D51D7')
    if hasattr(response, 'errors'):
        print '. '.join(response.errors)
    else:
        print 'Total Found: {}'.format(response.total)
        for i, activity in enumerate(response.results):
            print 'Activity #{}'.format(i + 1)
            print '\tActivity ID: {}'.format(activity.activity_id)
            print '\tActivity Message: {}'.format(activity.activity_message)
            print '\tActivity Type: {}'.format(activity.activity_type)
            print '\tRoute ID: {}'.format(activity.route_id)
            print '\tRoute Name: {}'.format(activity.route_name)


if __name__ == '__main__':
    main()
# codebeat:enable[SIMILARITY]
