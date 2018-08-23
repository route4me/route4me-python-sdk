# -*- coding: utf-8 -*-

# codebeat:disable[SIMILARITY]
from route4me import Route4Me

KEY = "11111111111111111111111111111111"


def main():
    route4me = Route4Me(KEY)
    avoidance_zones = route4me.avoidance_zones
    print('Creating Circle Shape Zone')
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
    response = avoidance_zones.add_avoidance_zone(**territory)
    if hasattr(response, 'errors'):
        print('. '.join(response.errors))
    else:
        print('Territory ID: {}'.format(response.territory_id))
        print('\tTerritory Name: {}'.format(response.territory_name))
        print('\tTerritory Color: {}'.format(response.territory_color))
        print('\tMember ID: {}'.format(response.member_id))
        print('\tTerritory Type: {}'.format(response.territory.type))
        if response.territory.data:
            print('\tData:')
            for data in response.territory.data:
                print('\t\t{0}'.format(data))


if __name__ == '__main__':
    main()
# codebeat:enable[SIMILARITY]
