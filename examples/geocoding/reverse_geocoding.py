# -*- coding: utf-8 -*-
from route4me import Route4Me

API_KEY = "11111111111111111111111111111111"


def main():
    route4me = Route4Me(API_KEY)
    coordinate = "42.35863,-71.05670"
    print('Getting Address from this coordinate: {}'.format(coordinate))
    response = route4me.address.geocode(addresses=coordinate)
    print(response)


if __name__ == '__main__':
    main()
