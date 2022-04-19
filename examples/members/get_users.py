# -*- coding: utf-8 -*-

import argparse

from route4me import Route4Me


def main(api_key):
    route4me = Route4Me(api_key)

    members = route4me.members
    response = members.get_users(limit=5, offset=0)
    if isinstance(response, dict) and 'errors' in response.keys():
        print('. '.join(response['errors']))
    else:
        for i, member in enumerate(response):
            print('Member #{}'.format(i + 1))
            print('\tName: {0}, {1}'.format(
                member.get('member_first_name'),
                member.get('member_last_name')
            ))
            print('\tEmail: {}'.format(member.get('member_email')))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Get All Users')
    parser.add_argument('--api_key', dest='api_key', help='Route4Me API KEY',
                        type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
