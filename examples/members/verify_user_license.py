# -*- coding: utf-8 -*-

from route4me import Route4Me

API_KEY = "11111111111111111111111111111111"


def main():
    route4me = Route4Me(API_KEY)
    members = route4me.members
    data = {
        "device_id": "1",
        "device_type": "ipad",
        "format": "json",
    }
    response = members.verify_device_license(**data)
    if isinstance(response, dict) and 'errors' in response.keys():
        print('. '.join(response['errors']))
    else:
        print(response)


if __name__ == '__main__':
    main()
