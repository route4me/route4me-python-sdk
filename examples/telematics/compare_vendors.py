# -*- coding: utf-8 -*-
import argparse

from route4me import Route4Me


def main(api_key):
    route4me = Route4Me(api_key)

    telematics = route4me.telematics
    vendors = telematics.compare_vendors('1,58,155')
    print('ID\tNAME\tFEATURES')
    for vendor in vendors.get('vendors', []):
        telematics.pp_vendor_comparison(vendor)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Telematics Vendors Comparison')
    parser.add_argument('--api_key', dest='api_key', help='Route4Me API KEY',
                        type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
