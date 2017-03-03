from route4me import Route4Me

KEY = "11111111111111111111111111111111"


def main():
    route4me = Route4Me(KEY)
    route = route4me.route
    response = route.get_routes(limit=10, Offset=5)
    if hasattr(response, 'errors'):
        print('. '.join(response.errors))
    else:
        response = route.get_route(route_id=response[0].route_id)
        if hasattr(response, 'errors'):
            print('. '.join(response.errors))
        else:
            route_id = response.route_id
            route_destination_id = response.addresses[0].route_destination_id
            response = route4me.address.get_address(
                route_id=route_id,
                route_destination_id=route_destination_id)
            if hasattr(response, 'errors'):
                print('. '.join(response.errors))
            else:
                print('Address: {}'.format(response.address))

if __name__ == '__main__':
    main()
