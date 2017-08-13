from route4me import Route4Me

KEY = "11111111111111111111111111111111"


def main():
    route4me = Route4Me(KEY)
    response = route4me.address.geocode(
        addresses="Boston-Cambridge-Quincy, MA-NH, USA"
    )
    print(response)


if __name__ == '__main__':
    main()
