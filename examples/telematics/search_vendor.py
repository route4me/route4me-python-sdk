# -*- coding: utf-8 -*-
import argparse

from route4me import Route4Me


def main(api_key):
    route4me = Route4Me(api_key)
    telematics = route4me.telematics
    print('****************************')
    print('Searching for Global Vendors')
    print('****************************')
    vendors = telematics.search_vendor(size='global', per_page=2, page=1)
    for vendor in vendors.get('vendors', []):
        telematics.pp_response(vendor)
    print('************************************')
    print('Searching Sattellite Feature Vendors')
    print('************************************')
    vendors = telematics.search_vendor(feature='Satellite', per_page=2, page=1)
    for vendor in vendors.get('vendors', []):
        telematics.pp_response(vendor)
    print('********************************')
    print('Searching for GB country Vendors')
    print('********************************')
    vendors = telematics.search_vendor(country='GB', per_page=2, page=1)
    for vendor in vendors.get('vendors', []):
        telematics.pp_response(vendor)

    print('**************************************')
    print('Searching Vendors with keyword "fleet"')
    print('**************************************')
    vendors = telematics.search_vendor(s='fleet', per_page=3, page=1)
    for vendor in vendors.get('vendors', []):
        telematics.pp_response(vendor)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Search Telematics Vendors')
    parser.add_argument('--api_key', dest='api_key', help='Route4Me API KEY',
                        type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
