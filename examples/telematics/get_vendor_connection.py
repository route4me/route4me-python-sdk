# -*- coding: utf-8 -*-
import argparse

from route4me import Route4Me


def main(api_token, connection_token):
    route4me = Route4Me(None)
    telematics = route4me.telematics
    vendor_connection = telematics.get_connection(api_token, connection_token)
    telematics.pp_response(vendor_connection)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Get Telematics Member Connection')
    parser.add_argument('--api_token', dest='api_token', help='Telematics API TOKEN',
                        type=str, required=True)
    parser.add_argument('--connection_token', dest='connection_token', help='Telematics Connection Token',
                        type=str, required=True)
    args = parser.parse_args()
    main(args.api_token, args.connection_token)
