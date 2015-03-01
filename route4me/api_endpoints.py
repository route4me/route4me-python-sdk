DRIVER_VERSION = 'route4me-python-driver-0.0.1'
MAIN_HOST = 'https://www.route4me.com'
API_HOST = '{0}/api.v4/optimization_problem.php'.format(MAIN_HOST)
SHOW_ROUTE_HOST = '{0}/route4me.php'.format(MAIN_HOST)
ROUTE_HOST = '{0}/api.v4/route.php'.format(MAIN_HOST)
SET_GPS_HOST = '{0}/track/set.php'.format(MAIN_HOST)
BATCH_GEOCODER = '{0}/api/geocoder.php'.format(MAIN_HOST)
SINGLE_GEOCODER = '{0}/api/address.php'.format(MAIN_HOST) 
EXPORTER = MAIN_HOST + '{0}/actions/route/export_current_route.php'

