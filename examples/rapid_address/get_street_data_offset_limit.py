# -*- coding: utf-8 -*-

import argparse

from route4me import Route4Me


def main(api_key):
    route4me = Route4Me(api_key)

    rapid_address = route4me.rapid_address
    response = rapid_address.get_street_data(offset=10, limit=10)
    if isinstance(response, dict) and 'errors' in response.keys():
        print('. '.join(response['errors']))
    elif not response:
        print("Unknown error occured")
    else:
        for street in response:
            print('Street Name:\t{0}\t\tZip Code:\t{1}'.format(
                street.get('street_name'),
                street.get('zipcode')))


if __name__ == '__main__':
    print("DEPRECATED - Service Not Available")

    parser = argparse.ArgumentParser(description='Get Street Addresses Using Limit and Offset')
    parser.add_argument('--api_key', dest='api_key', help='Route4Me API KEY',
                        type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
