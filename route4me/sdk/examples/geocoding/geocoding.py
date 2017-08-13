from route4me import Route4Me

KEY = "11111111111111111111111111111111"


def main():
    route4me = Route4Me(KEY)
    addresses = [{'address': '455 S 4th St, Louisville, KY 40202'},
                 {'address': '1604 PARKRIDGE PKWY, Louisville, KY, 40214'},
                 {'address': '1407 MCCOY, Louisville, KY, 40215'},
                 {'address': '4805 BELLEVUE AVE, Louisville, KY, 40215'},
                 {'address': '730 CECIL AVENUE, Louisville, KY, 40211'}, ]
    for address in addresses:
        print('Original Address: {0}'.format(address))
        geocode_error, address = route4me.address.fix_geocode(address)
        if geocode_error:
            print('Geocoding Error: {0}'.format(geocode_error))
        print('Geocoded Address: {0}'.format(address))


if __name__ == '__main__':
    main()
