#!/usr/bin/python

from route4me import Route4Me

KEY = "11111111111111111111111111111111"


def main():
    route4me = Route4Me(KEY)
    route = route4me.route
    print route.get_route(route_id='AC16E7D338B551013FF34266FE81A5EE')

if __name__ == '__main__':
    main()
