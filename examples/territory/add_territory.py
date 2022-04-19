# -*- coding: utf-8 -*-
# codebeat:disable[SIMILARITY, LOC, ABC]

import argparse

from route4me import Route4Me


def main(api_key):
    route4me = Route4Me(api_key)

    territories = route4me.territory
    print('Creating Poly Territory')
    territory = {
        "territory_name": "Polygon Territory",
        "territory_color": "ff0000",
        "territory": {
            "type": "poly",
            "data": [
                "56.127184156131065,56.93115234375",
                "58.41322259056806,59.501953125",
                "61.53840616716746,59.315185546875",
                "61.047650586031104,51.998291015625",
                "59.254649544483726,53.63525390625",
                "56.47462805805596,54.42626953125"
            ]
        }
    }
    response = territories.add_territory(**territory)
    if isinstance(response, dict) and 'errors' in response.keys():
        print('. '.join(response['errors']))
    else:
        print('Territory ID: {}'.format(response['territory_id']))
        print('\tTerritory Name: {}'.format(response['territory_name']))
        print('\tTerritory Color: {}'.format(response['territory_color']))
        print('\tMember ID: {}'.format(response['member_id']))
        print('\tTerritory Type: {}'.format(response['territory']['type']))
        if response['territory']['data']:
            print('\tData:')
            for data in response['territory']['data']:
                print('\t\t{0}'.format(data))
    print('Creating Circle Territory')
    territory = {
        "territory_name": "Circle Territory",
        "territory_color": "ff0000",
        "territory": {
            "type": "circle",
            "data": [
                "37.569752822786455,-77.47833251953125",
                "5000",
            ]
        }
    }
    response = territories.add_territory(**territory)
    if isinstance(response, dict) and 'errors' in response.keys():
        print('. '.join(response['errors']))
    else:
        print('Territory ID: {}'.format(response['territory_id']))
        print('\tTerritory Name: {}'.format(response['territory_name']))
        print('\tTerritory Color: {}'.format(response['territory_color']))
        print('\tMember ID: {}'.format(response['member_id']))
        print('\tTerritory Type: {}'.format(response['territory']['type']))
        if response['territory']['data']:
            print('\tData:')
            for data in response['territory']['data']:
                print('\t\t{0}'.format(data))
    print('Creating Rect Territory')
    territory = {
        "territory_name": "Rect Territory",
        "territory_color": "ff0000",
        "territory": {
            "type": "rect",
            "data": [
                "43.51668853502909,-109.3798828125",
                "46.98025235521883,-101.865234375"
            ]
        }
    }
    response = territories.add_territory(**territory)
    if isinstance(response, dict) and 'errors' in response.keys():
        print('. '.join(response['errors']))
    else:
        print('Territory ID: {}'.format(response['territory_id']))
        print('\tTerritory Name: {}'.format(response['territory_name']))
        print('\tTerritory Color: {}'.format(response['territory_color']))
        print('\tMember ID: {}'.format(response['member_id']))
        print('\tTerritory Type: {}'.format(response['territory']['type']))
        if response['territory']['data']:
            print('\tData:')
            for data in response['territory']['data']:
                print('\t\t{0}'.format(data))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Add Territory')
    parser.add_argument('--api_key', dest='api_key', help='Route4Me API KEY',
                        type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)

    # codebeat:enable[SIMILARITY, LOC, ABC]
