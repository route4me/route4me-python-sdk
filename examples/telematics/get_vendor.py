# -*- coding: utf-8 -*-
import argparse

from route4me import Route4Me


def main(api_key, vendor_id):
    route4me = Route4Me(api_key)

    telematics = route4me.telematics
    vendor = telematics.get_vendor(vendor_id)
    telematics.pp_response(vendor.get('vendor', {}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Get Telematics Vendors')
    parser.add_argument('--api_key', dest='api_key', help='Route4Me API KEY',
                        type=str, required=True)
    parser.add_argument('--vendor_id', dest='vendor_id', help='Telematics Vendor ID',
                        type=int, required=True)
    args = parser.parse_args()
    main(args.api_key, args.vendor_id)
