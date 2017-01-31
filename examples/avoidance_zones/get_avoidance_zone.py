from route4me import Route4Me
from route4me.constants import *

KEY = "11111111111111111111111111111111"

# codebeat:disable[SC]
def main():
    route4me = Route4Me(KEY)
    avoidance_zones = route4me.avoidance_zones
    response = avoidance_zones.get_avoidance_zones()
    if hasattr(response, 'errors'):
        print '. '.join(response.errors)
    else:
        territory_id = response[0].territory_id
        print 'Getting Territory ID: {}'.format(territory_id)
        response = avoidance_zones.get_avoidance_zone(territory_id=territory_id)
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
# codebeat:enable[SC]