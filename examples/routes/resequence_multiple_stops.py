# -*- coding: utf-8 -*-
import argparse
import json

from route4me import Route4Me


def load_json(filename):
    data = []
    with open(filename, 'rt') as datafile:
        data = json.load(datafile)
        datafile.close()
    return data


def main(args):
    r4m = Route4Me(args.api_key)
    route_data = load_json(args.route_data_filename)
    route = r4m.route
    print(f'Route ID: {args.route_id}')
    print("Addresses to be Re-sequence")
    for address in route_data['addresses']:
        print(f'Address Sequence: {address["sequence_no"]:6} - '
              f'Route Destination ID: {address["route_destination_id"]:9}')
    print(f"After Resequence the Route {args.route_id}")
    response_data = route.resequence_multiple_stops(args.route_id, route_data)
    for address in response_data['addresses']:
        print(f'Address Sequence: {address["sequence_no"]:6} - '
              f'Route Destination ID: {address["route_destination_id"]:9} - Address: {address["address"]} ')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Resequence a Route')
    parser.add_argument('--api_key', dest='api_key', help='Route4Me API KEY',
                        type=str, required=True)
    parser.add_argument('--route_id', dest='route_id', help='Route ID',
                        type=str, required=True)
    parser.add_argument('--route_data_filename', dest='route_data_filename',
                        help='JSON file name with Route Addresses ID and Sequence',
                        type=str, required=True)
    args = parser.parse_args()
    main(args)
