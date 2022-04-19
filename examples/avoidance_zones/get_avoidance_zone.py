# -*- coding: utf-8 -*-
# codebeat:disable[SIMILARITY, BLOCK_NESTING]

import argparse

from route4me import Route4Me


def main(api_key):
    route4me = Route4Me(api_key)

    avoidance_zones = route4me.avoidance_zones
    response = avoidance_zones.get_avoidance_zones()
    if isinstance(response, dict) and 'errors' in response.keys():
        print('. '.join(response['errors']))
    else:
        territory_id = response[0]['territory_id']
        print('Getting Territory ID: {}'.format(territory_id))
        response = avoidance_zones.get_avoidance_zone(territory_id=territory_id)
        if isinstance(response, dict) and 'errors' in response.keys():
            print('. '.join(response['errors']))
        else:
            print('Territory ID: {}'.format(response['territory_id']))
            print('\tTerritory Name: {}'.format(response['territory_name']))
            print('\tTerritory Color: {}'.format(response['territory_color']))
            print('\tMember ID: {}'.format(response['member_id']))
            print('\tTerritory Type: {}'.format(response['territory']['type']))
            if response['territory']['data']:
                print('\tData: ')
                for data in response['territory']['data']:
                    print('\t\t{0}'.format(data))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Get Avoidance Zone')
    parser.add_argument('--api_key', dest='api_key', help='Route4Me API KEY',
                        type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)

# codebeat:enable[SIMILARITY, BLOCK_NESTING]
