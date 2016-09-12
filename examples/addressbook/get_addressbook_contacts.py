from route4me import Route4Me
from route4me.constants import *

KEY = "11111111111111111111111111111111"


def main():
    route4me = Route4Me(KEY)
    address_book = route4me.address_book
    response = address_book.get_addressbook_contacts(limit=10, Offset=5)
    if 'errors' in response.keys():
        print '. '.join(response['errors'])
    else:
        contacts = response['results']
        for i, contact in enumerate(contacts):
            print 'Address: {0} -  ID: {1}'.format(i+1, contact['address_id'])
            print '\tFirst Name: {0}'.format(contact['first_name'])
            print '\tLast Name: {0}'.format(contact['last_name'])
            print '\tAddress: {0}'.format(contact['address_1'])


if __name__ == '__main__':
    main()
