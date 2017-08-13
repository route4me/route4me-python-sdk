from route4me import Route4Me

KEY = "11111111111111111111111111111111"


def main():
    route4me = Route4Me(KEY)
    response = route4me.address.geocode(addresses="42.35863,-71.05670")
    print(response)


if __name__ == '__main__':
    main()
