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
                "disable_optimization": 0,
                "optimize": 'Distance',
                "route_id": response.route_id,
            }
            response = route.resequence_route_all(**data)
            print(response)


if __name__ == '__main__':
    main()
