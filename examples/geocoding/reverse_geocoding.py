# -*- coding: utf-8 -*-
import argparse

from route4me import Route4Me


def main(api_key):
    route4me = Route4Me(api_key)

    coordinate = "42.35863,-71.05670"
    print('Getting Address from this coordinate: {}'.format(coordinate))
    response = route4me.address.geocode(addresses=coordinate)
    print(response)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Reverse Geocoding')
    parser.add_argument('--api_key', dest='api_key', help='Route4Me API KEY',
                        type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
