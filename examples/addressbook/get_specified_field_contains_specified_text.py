# -*- coding: utf-8 -*-
import argparse

from route4me import Route4Me


def main(api_key):
    route4me = Route4Me(api_key)

    address_book = route4me.address_book
    print('Searching "Juan" in Addressbook')
    response = address_book.get_addressbook_contacts(
        limit=10,
        offset=0,
        query='juan',
        fields='first_name,address_email'
    )
    for row in response.get('results', []):
        print('First Name: {} - Email: {}'.format(*row))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Search Contact by Field and Value')
    parser.add_argument('--api_key', dest='api_key', help='Route4Me API KEY',
                        type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
