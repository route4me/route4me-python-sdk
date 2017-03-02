from route4me import Route4Me

KEY = "11111111111111111111111111111111"


def main():
    route4me = Route4Me(KEY)
    vehicles = route4me.vehicles
    response = vehicles.get_vehicles()
    if type(response) == dict and 'errors' in response.keys():
        print ('. '.join(response.get('errors')))
    else:
        for vehicle in response:
            print ('Vehicle ID: {0}\tVehicle Alias: {1}'.format(
                vehicle.get('vehicle_id'),
                vehicle.get('vehicle_alias')
            ))


if __name__ == '__main__':
    main()
