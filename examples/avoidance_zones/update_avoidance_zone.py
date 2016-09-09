#!/usr/bin/python

from route4me import Route4Me
from route4me.constants import *

KEY = "11111111111111111111111111111111"


def main():
    route4me = Route4Me(KEY)
    avoidance_zones = route4me.avoidance_zones
    print 'Creating Poly Zone'
    territory = {"territory_name": "Polygon Territory",
                 "territory_color": "ff0000",
                 "territory": {"type": "poly",
                               "data": ["56.127184156131065,56.93115234375",
                                        "58.41322259056806,59.501953125",
                                        "61.53840616716746,59.315185546875",
                                        "61.047650586031104,51.998291015625",
                                        "59.254649544483726,53.63525390625",
                                        "56.47462805805596,54.42626953125"
                                        ]
                               }
                 }
    response = avoidance_zones.add_avoidance_zone(**territory)
    if hasattr(response, 'errors'):
        print '. '.join(response.errors)
    else:
        territory_id = response.territory_id
        print 'Territory ID: {0} -> Created'.format(territory_id)
        print '\tTerritory Name: {}'.format(response.territory_name)
        print '\tTerritory Color: {}'.format(response.territory_color)
        print '\tMember ID: {}'.format(response.member_id)
        print '\tTerritory Type: {}'.format(response.territory.type)
        if response.territory.data:
            print '\tData: '
            for data in response.territory.data:
                print '\t\t{0}'.format(data)
        territory = {"territory_name": "Polygon Territory Updated",
                     "territory_color": "ff00ff",
                     "territory": {"type": "poly",
                                   "data": ["56.127184156131065,56.93115234375",
                                            "58.41322259056806,59.501953125",
                                            "61.53840616716746,59.315185546875",
                                            "61.047650586031104,51.998291015625",
                                            "59.254649544483726,53.63525390625",
                                            "56.47462805805596,54.42626953125"
                                            ]
                                   }
                     }
        response = avoidance_zones.update_avoidance_zone(territory_id=territory_id, **territory)
        if hasattr(response, 'errors'):
            print '. '.join(response.errors)
        else:
            print 'Territory ID: {}'.format(response.territory_id)
            print '\tTerritory Name: {}'.format(response.territory_name)
            print '\tTerritory Color: {}'.format(response.territory_color)
            print '\tMember ID: {}'.format(response.member_id)
            print '\tTerritory Type: {}'.format(response.territory.type)
            if response.territory.data:
                print '\tData: '
                for data in response.territory.data:
                    print '\t\t{0}'.format(data)

if __name__ == '__main__':
    main()
