from route4me import Route4Me

KEY = "11111111111111111111111111111111"


def main():
    route4me = Route4Me(KEY)
    activity_feed = route4me.activity_feed
    response = activity_feed.log_specific_message(activity_message='Hello from Python SDK',
                                                  route_id='D2F447BCB1F8B8388E88B07188B3A256')
    if hasattr(response, 'errors'):
        print '. '.join(response.errors)
    else:
        print 'Message Logged: {}'.format(response.status)


if __name__ == '__main__':
    main()
