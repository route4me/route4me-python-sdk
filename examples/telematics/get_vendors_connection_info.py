# -*- coding: utf-8 -*-
import argparse

from route4me import Route4Me


def main(api_key, member_id):
    route4me = Route4Me(api_key)
    telematics = route4me.telematics
    token = telematics.register_member(member_id)

    if 'api_token' not in token.keys():
        print(token)
        return

    api_token = token['api_token']
    vendor_connections = telematics.get_vendors_info(api_token)
    for vendor_connection in vendor_connections:
        telematics.pp_response(vendor_connection)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Get Telematics Vendors Connection Information')
    parser.add_argument('--api_key', dest='api_key', help='Route4Me API KEY',
                        type=str, required=True)
    parser.add_argument('--member_id', dest='member_id', help='Route4Me member_id',
                        type=str, required=True)
    args = parser.parse_args()
    main(args.api_key, args.member_id)
