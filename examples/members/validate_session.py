# -*- coding: utf-8 -*-
import argparse

from route4me import Route4Me


def main(api_key):
    route4me = Route4Me(api_key)

    members = route4me.members
    data = {
        "session_guid": "4552222222",
        "member_id": "1",
        "format": "json"
    }
    response = members.validate_session(**data)
    if isinstance(response, dict) and 'errors' in response.keys():
        print('. '.join(response['errors']))
    else:
        print(response)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Validate Session')
    parser.add_argument('--api_key', dest='api_key', help='Route4Me API KEY',
                        type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
