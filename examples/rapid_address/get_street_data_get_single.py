from route4me import Route4Me

KEY = "11111111111111111111111111111111"


def main():
    route4me = Route4Me(KEY)
    rapid_address = route4me.rapid_address
    response = rapid_address.get_street_data(pk=33)
    print 'Street Name:\t{0}\t\tZip Code:\t{1}'.format(
        response.get('street_name'),
        response.get('zipcode'))

if __name__ == '__main__':
    main()
