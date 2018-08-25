# -*- coding: utf-8 -*-

from route4me import Route4Me

API_KEY = "11111111111111111111111111111111"


def main():
    route4me = Route4Me(API_KEY)
    members = route4me.members
    data = {
        "email_address": "john@route4me.com",
        "first_name": "Jhon",
        "last_name": "Route4Me",
        "check_terms": "1",
        "industry": "Python SDK",
        "device_type": "web",
        "plan": "enterprise_plan",
        "password_1": "ultrasecret",
        "password_2": "ultrasecret",
        "format": "json",
    }
    response = members.register(**data)
    if isinstance(response, dict) and 'errors' in response.keys():
        print('. '.join(response['errors']))
    else:
        print(response)


if __name__ == '__main__':
    main()
