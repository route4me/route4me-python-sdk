# -*- coding: utf-8 -*-

import argparse

from route4me import Route4Me


def main(api_key):
    route4me = Route4Me(api_key)

    members = route4me.members
    data = {
        "member_id": 1,
        "session_guid": "454563",
        "device_id": "54564",
        "device_type": "ipad",
        "subscription_name": "IPAD_MONTHLY",
        "token": "4/P7q7W91a-oMsCeLvIaQm6bTrgtp7",
        "payload": "APA91bHun4MxP5egoKMwt2KZFBaFUH-1RYqx",
        "format": "json",
    }
    response = members.app_purchase_user_license(**data)
    if isinstance(response, dict) and 'errors' in response.keys():
        print('. '.join(response['errors']))
    else:
        print(response)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='App Purchase user License')
    parser.add_argument('--api_key', dest='api_key', help='Route4Me API KEY',
                        type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
