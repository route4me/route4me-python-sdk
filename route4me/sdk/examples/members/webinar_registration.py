from route4me import Route4Me

KEY = "11111111111111111111111111111111"


def main():
    route4me = Route4Me(KEY)
    members = route4me.members
    data = {
        "email_address": "john@route4me.com",
        "first_name": "Jhon",
        "last_name": "Route4Me",
        "phone_number": "454-454544",
        "company_name": "Python SDK",
        "member_id": "123456",
        "webiinar_date": "2016-09-16 02:48:00",
    }
    response = members.webinar_registration(**data)
    if hasattr(response, 'errors'):
        print('. '.join(response.errors))
    else:
        print(response)


if __name__ == '__main__':
    main()
