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
                "addresses": [{
                    "address": "Cabo Rojo, Cabo Rojo 00623, Puerto Rico",
                    "alias": "Cabo Rojo, Cabo Rojo 00623, Puerto Rico",
                    "lat": 18.086627,
                    "lng": -67.145735,
                    "curbside_lat": 18.086627,
                    "curbside_lng": -67.145735,
                    "contact_id": False,
                    "is_departed": False,
                    "is_visited": False,
                }],
                "optimal_position": True,
                "route_id": response.route_id
            }
            response = route.insert_address_into_route_optimal_position(**data)
            print('Optimization Problem ID: {}'.format(
                response.optimization_problem_id
            ))
            print('Route ID: {}'.format(response.route_id))
            for i, address in enumerate(response.addresses):
                print('Address #{}'.format(i))
                print('\tAddress: {0}'.format(address.address))
                print('\tRoute Destination ID: {0}'.format(
                    address.route_destination_id
                ))


if __name__ == '__main__':
    main()
