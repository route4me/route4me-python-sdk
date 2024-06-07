# -*- coding: utf-8 -*-

import argparse

from route4me import Route4Me


def main(api_key):
    route4me = Route4Me(api_key)

    addresses = [{'address': '455 S 4th St, Louisville, KY 40202'},
                 {'address': '1604 PARKRIDGE PKWY, Louisville, KY, 40214'},
                 {'address': '1407 MCCOY, Louisville, KY, 40215'},
                 {'address': '4805 BELLEVUE AVE, Louisville, KY, 40215'},
                 {'address': '730 CECIL AVENUE, Louisville, KY, 40211'}, ]
    for address in addresses:
        print('Original Address: {0}'.format(address))
        geocode_error, address = route4me.address.fix_geocode(address)
        if geocode_error:
            print('Geocoding Error: {0}'.format(geocode_error))
        print('Geocoded Address: {0}'.format(address))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Geocoding')
    parser.add_argument('--api_key', dest='api_key', help='Route4Me API KEY',
                        type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
