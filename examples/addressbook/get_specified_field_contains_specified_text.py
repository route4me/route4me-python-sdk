# -*- coding: utf-8 -*-
from route4me import Route4Me

KEY = "11111111111111111111111111111111"


def main():
    route4me = Route4Me(KEY)
    address_book = route4me.address_book
    response = address_book.get_addressbook_contacts(
        limit=10,
        offset=0,
        query='juan',
        fields='first_name,address_email'
    )
    for row in response.get('results', []):
        print('Firt Name: {} - Email: {}'.format(*row))


if __name__ == '__main__':
    main()
