from route4me import Route4Me

KEY = "11111111111111111111111111111111"


def main():
    route4me = Route4Me(KEY)
    route = route4me.route
    response = route.get_routes(limit=10, Offset=5)
    if hasattr(response, 'errors'):
        print '. '.join(response.errors)
    else:
        for i, route in enumerate(response):
            print('Route #{}'.format(i + 1))
            print('\tOptimization Problem ID: {}'.format(
                route.optimization_problem_id))
            print('\tRoute ID: {}'.format(route.route_id))

if __name__ == '__main__':
    main()
