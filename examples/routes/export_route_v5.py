# -*- coding: utf-8 -*-
import argparse

from route4me import Route4Me


def main(api_key, route_id):
    route4me = Route4Me(api_key)

    route = route4me.route
    exported_route = route.export_route_v5(route_id)

    print(exported_route)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Route Exporter API V5')
    parser.add_argument('--api_key', dest='api_key', help='Route4Me API KEY',
                        type=str, required=True)
    parser.add_argument('--route_id', dest='route_id', help='Route ID',
                        type=str, required=True)
    args = parser.parse_args()
    main(args.api_key, args.route_id)
