import argparse

from route4me import Route4Me


def main(api_key):
    route4me = Route4Me(api_key)

    address_book = route4me.address_book
    response = address_book.create_contact(
        first_name="Juan",
        last_name="Pimentel",
        address_1="17205 RICHMOND TNPK, MILFORD, VA, 22514",
        cached_lat=38.024654,
        cached_lng=-77.338814,
    )
    print(f"Address ID: {response['address_id']}")
    print(f"First Name: {response['first_name']}")
    print(f"Last Name: {response['last_name']}")
    print(f"Address: {response['address_1']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Add AddressBook Contact")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
