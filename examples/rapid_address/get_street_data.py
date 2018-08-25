# -*- coding: utf-8 -*-

from route4me import Route4Me

API_KEY = "11111111111111111111111111111111"


def main():
    route4me = Route4Me(API_KEY)
    rapid_address = route4me.rapid_address
    response = rapid_address.get_street_data()
    for street in response:
        print('Street Name:\t{0}\t\tZip Code:\t{1}'.format(
            street.get('street_name'),
            street.get('zipcode')))


if __name__ == '__main__':
    main()
