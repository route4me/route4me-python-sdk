from route4me import Route4Me

KEY = "11111111111111111111111111111111"


def main():
    route4me = Route4Me(KEY)
    route = route4me.route
    response = route.get_routes(limit=10, Offset=5)
    if hasattr(response, 'errors'):
        print('. '.join(response.errors))
    else:
        response = route.get_activities(route_id=response[0].route_id,
                                        limit=10,
                                        Offset=5)
        if hasattr(response, 'errors'):
            print('. '.join(response.errors))
        else:
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
