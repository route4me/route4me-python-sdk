# -*- coding: utf-8 -*-

import argparse

from route4me import Route4Me


def main(api_key):
    route4me = Route4Me(api_key)

    address_book = route4me.address_book
    response = address_book.get_addressbook_contacts(limit=10, offset=5)
    if isinstance(response, dict) and 'errors' in response.keys():
        print('. '.join(response['errors']))
    else:
        address_id = "'{}'".format(response['results'][0]['address_id'])
        response = address_book.get_addressbook_contact(address_id=address_id)
        if isinstance(response, dict) and 'errors' in response.keys():
            print('. '.join(response['errors']))
        else:
            contacts = response['results']
            for i, contact in enumerate(contacts):
                print('Address: {0} -  ID: {1}'.format(i + 1,
                                                       contact['address_id']))
                print('\tFirst Name: {0}'.format(contact['first_name']))
                print('\tLast Name: {0}'.format(contact['last_name']))
                print('\tAddress: {0}'.format(contact['address_1']))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Get Address Book Contact')
    parser.add_argument('--api_key', dest='api_key', help='Route4Me API KEY',
                        type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
