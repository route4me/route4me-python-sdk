# -*- coding: utf-8 -*-
import argparse

from route4me import Route4Me


def main(api_key):
    route4me = Route4Me(api_key)

    rapid_address = route4me.rapid_address
    response = rapid_address.get_street_data(pk=33)
    if isinstance(response, dict) and 'errors' in response.keys():
        print('. '.join(response['errors']))
    else:
        print('Street Name:\t{0}\t\tZip Code:\t{1}'.format(
            response.get('street_name'),
            response.get('zipcode')))


if __name__ == '__main__':
    print("DEPRECATED - Service Not Available")
    parser = argparse.ArgumentParser(description='Get Street Address by ID')
    parser.add_argument('--api_key', dest='api_key', help='Route4Me API KEY',
                        type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
