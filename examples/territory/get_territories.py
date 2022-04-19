# -*- coding: utf-8 -*-
# codebeat:disable[SIMILARITY, BLOCK_NESTING]

import argparse

from route4me import Route4Me


def main(api_key):
    route4me = Route4Me(api_key)

    territory = route4me.territory
    response = territory.get_territories()
    if isinstance(response, dict) and 'errors' in response.keys():
        print('. '.join(response['errors']))
    else:
        for i, territory in enumerate(response):
            print('{0}  - Territory ID: {1}'.format(i + 1,
                                                    territory['territory_id']))
            print('\tTerritory Name: {}'.format(territory['territory_name']))
            print('\tTerritory Color: {}'.format(territory['territory_color']))
            print('\tMember ID: {}'.format(territory['member_id']))
            print('\tTerritory Type: {}'.format(territory['territory']['type']))
            if territory['territory']['data']:
                print('\tData:')
                for data in territory['territory']['data']:
                    print('\t\t{0}'.format(data))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Get Multiple Territories')
    parser.add_argument('--api_key', dest='api_key', help='Route4Me API KEY',
                        type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)

# codebeat:enable[SIMILARITY, BLOCK_NESTING]
