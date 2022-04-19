# -*- coding: utf-8 -*-
import argparse
import json

from route4me import Route4Me


def _load_credentials(fn):
    with open(fn, 'rt') as inputfile:
        data = json.load(inputfile)
        inputfile.close()
        return data


def main(api_token, connection_token, filename):
    route4me = Route4Me(None)
    telematics = route4me.telematics
    vendor_credentials = _load_credentials(filename)
    vendor_connection = telematics.update_connection(api_token, connection_token, **vendor_credentials)
    telematics.pp_response(vendor_connection)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Update Telematics Member Connection')
    parser.add_argument('--api_token', dest='api_token', help='Telematics API TOKEN',
                        type=str, required=True)
    parser.add_argument('--connection_token', dest='connection_token', help='Telematics Connection Token',
                        type=str, required=True)
    parser.add_argument('--vendor_credentials', dest='filename',
                        help='filename of the JSON with Telematics Vendor Credentials',
                        type=str, required=True)
    args = parser.parse_args()
    main(args.api_token, args.connection_token, args.filename)
