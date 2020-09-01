# -*- coding: utf-8 -*-
import argparse
import json
from route4me import Route4Me


def _load_credentials(fn):
    with open(fn, 'rt') as inputfile:
        data = json.load(inputfile)
        inputfile.close()
        return data


def main(api_key, member_id, filename):
    route4me = Route4Me(api_key)
    telematics = route4me.telematics
    token = telematics.register_member(member_id)

    if 'api_token' not in token.keys():
        print(token)
        return

    api_token = token['api_token']
    vendor_credentials = _load_credentials(filename)
    vendor_connection = telematics.register_connection(api_token, **vendor_credentials)
    telematics.pp_response(vendor_connection)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Register Telematics Member Connection')
    parser.add_argument('--api_key', dest='api_key', help='Route4Me API KEY',
                        type=str, required=True)
    parser.add_argument('--member_id', dest='member_id', help='Route4Me member_id',
                        type=str, required=True)
    parser.add_argument('--vendor_credentials', dest='filename',
                        help='filename of the JSON with Telematics Vendor Credentials',
                        type=str, required=True)
    args = parser.parse_args()
    main(args.api_key, args.member_id, args.filename)
