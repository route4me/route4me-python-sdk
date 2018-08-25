# -*- coding: utf-8 -*-

from route4me import Route4Me

API_KEY = "11111111111111111111111111111111"


def main():
    route4me = Route4Me(API_KEY)
    address = "Boston-Cambridge-Quincy, MA-NH, USA"
    print('Geocoding this address: {}'.format(address))
    response = route4me.address.geocode(
        addresses=address
    )
    print(response)


if __name__ == '__main__':
    main()
