# codebeat:disable[SIMILARITY, BLOCK_NESTING]
from route4me import Route4Me

KEY = "11111111111111111111111111111111"


def main():
    route4me = Route4Me(KEY)
    territory = route4me.territory
    response = territory.get_territories()
    if hasattr(response, 'errors'):
        print('. '.join(response.errors))
    else:
        for i, territory in enumerate(response):
            print('{0}  - Territory ID: {1}'.format(i + 1,
                                                    territory.territory_id))
            print('\tTerritory Name: {}'.format(territory.territory_name))
            print('\tTerritory Color: {}'.format(territory.territory_color))
            print('\tMember ID: {}'.format(territory.member_id))
            print('\tTerritory Type: {}'.format(territory.territory.type))
            if territory.territory.data:
                print('\tData:')
                for data in territory.territory.data:
                    print('\t\t{0}'.format(data))


if __name__ == '__main__':
    main()
# codebeat:enable[SIMILARITY, BLOCK_NESTING]
