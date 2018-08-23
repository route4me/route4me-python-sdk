# -*- coding: utf-8 -*-

from route4me import Route4Me

API_KEY = "11111111111111111111111111111111"


def main():
    route4me = Route4Me(API_KEY)
    address_book = route4me.address_book
    response = address_book.get_addressbook_contacts(limit=10, offset=5)
    if 'errors' in response.keys():
        print('. '.join(response['errors']))
    else:
        address_id = "'{}'".format(response['results'][0]['address_id'])
        response = address_book.get_addressbook_contact(address_id=address_id)
        if 'errors' in response.keys():
            print('. '.join(response['errors']))
        else:
            contact = response['results'][0]
            contact['first_name'] = '{} Updated'.format(contact['first_name'])
            response = address_book.update_contact(**contact)
            if 'errors' in response.keys():
                print('. '.join(response['errors']))
            else:
                print('Address ID: {0}'.format(response['address_id']))
                print('First Name: {0}'.format(response['first_name']))
                print('Last Name: {0}'.format(response['last_name']))
                print('Address: {0}'.format(response['address_1']))


if __name__ == '__main__':
    main()
