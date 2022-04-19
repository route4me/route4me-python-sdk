# -*- coding: utf-8 -*-

import argparse

from route4me import Route4Me


def main(api_key):
    route4me = Route4Me(api_key)

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
    if isinstance(response, dict) and 'errors' in response.keys():
        print('. '.join(response['errors']))
    else:
        print(response)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Webinar Registration')
    parser.add_argument('--api_key', dest='api_key', help='Route4Me API KEY',
                        type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
