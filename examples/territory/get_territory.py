# -*- coding: utf-8 -*-
# codebeat:disable[SIMILARITY, BLOCK_NESTING]

from route4me import Route4Me

API_KEY = "11111111111111111111111111111111"


def main():
    route4me = Route4Me(API_KEY)
    territories = route4me.territory
    response = territories.get_territories()
    if isinstance(response, dict) and 'errors' in response.keys():
        print('. '.join(response['errors']))
    else:
        territory_id = response[0]['territory_id']
        print('Getting Territory ID: {}'.format(territory_id))
        response = territories.get_territory(territory_id=territory_id)
        if isinstance(response, dict) and 'errors' in response.keys():
            print('. '.join(response['errors']))
        else:
            territory = response
            print('Territory ID: {0}'.format(territory['territory_id']))
            print('\tTerritory Name: {}'.format(territory['territory_name']))
            print('\tTerritory Color: {}'.format(territory['territory_color']))
            print('\tMember ID: {}'.format(territory['member_id']))
            print('\tTerritory Type: {}'.format(territory['territory']['type']))
            if territory['territory']['data']:
                print('\tData:')
                for data in territory['territory']['data']:
                    print('\t\t{0}'.format(data))


if __name__ == '__main__':
    main()
# codebeat:enable[SIMILARITY, BLOCK_NESTING]
