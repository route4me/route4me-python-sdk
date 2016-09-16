from route4me import Route4Me

KEY = "11111111111111111111111111111111"


def main():
    route4me = Route4Me(KEY)
    members = route4me.members
    data = {"email": "john@route4me.com",
            "password": "ultrasecretword",
            "format": "json"}
    response = members.member_authenticate(**data)
    if hasattr(response, 'errors'):
        print '. '.join(response.errors)
    else:
        print response


if __name__ == '__main__':
    main()
