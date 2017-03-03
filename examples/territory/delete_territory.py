# codebeat:disable[SIMILARITY]
from route4me import Route4Me

KEY = "11111111111111111111111111111111"


def main():
    route4me = Route4Me(KEY)
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
    if hasattr(response, 'errors'):
        print('. '.join(response.errors))
    else:
        territory_id = response.territory_id
        print('Territory ID: {0} -> Created'.format(territory_id))
        response = territories.delete_territory(territory_id=territory_id)
        if hasattr(response, 'errors'):
            print('. '.join(response.errors))
        else:
            print('Territory ID: {0} -> Deleted: {1}'.format(territory_id,
                                                             response.status))


if __name__ == '__main__':
    main()
# codebeat:enable[SIMILARITY]
