from route4me import Route4Me

KEY = "11111111111111111111111111111111"


def main():
    route4me = Route4Me(KEY)
    address_book = route4me.address_book
    response = address_book.create_contact(
        first_name="Juan",
        last_name="Pimentel",
        address_1="17205 RICHMOND TNPK, MILFORD, VA, 22514",
        cached_lat=38.024654,
        cached_lng=-77.338814,
    )
    if hasattr(response, 'errors'):
        print('. '.join(response.errors))
    else:
        print('Address ID: {0}'.format(response.address_id))
        print('First Name: {0}'.format(response.first_name))
        print('Last Name: {0}'.format(response.last_name))
        print('Address: {0}'.format(response.address_1))
        print('Deleting this Contact')
        address_ids = [response.address_id, ]
        response = address_book.delete_addressbook_contact(
            address_ids=address_ids)
        if hasattr(response, 'errors'):
            print('. '.join(response.errors))
        else:
            print('Deleted: {}'.format(response.status))


if __name__ == '__main__':
    main()
