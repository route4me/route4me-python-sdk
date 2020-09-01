.. include:: common.rst

Quick Start
===========

Quick start guide

Install
-------

Probably, the best and simplest way --- use PIP:

.. code-block:: bash

    $ pip install route4me-sdk

.. seealso::

	The full installation guide: :doc:`/install`

Use
---

.. code-block:: python

    from route4me import Route4Me
    from route4me.constants import ALGORITHM_TYPE, DISTANCE_UNIT, TRAVEL_MODE, OPTIMIZE

    API_KEY = "11111111111111111111111111111111"
    r4m = Route4Me(API_KEY)
    optimization = r4m.optimization
    address = r4m.address
    optimization.algorithm_type(ALGORITHM_TYPE.TSP)
    optimization.share_route(0)
    optimization.store_route(0)
    optimization.route_time(7 * 600)
    optimization.rt(True)
    optimization.route_max_duration(86400)
    optimization.route_name('Single Driver Round Trip')
    optimization.optimize(OPTIMIZE.TIME)
    optimization.distance_unit(DISTANCE_UNIT.MI)
    optimization.travel_mode(TRAVEL_MODE.DRIVING)
    address.add_address(
        address='754 5th Ave New York, NY 10019',
        lat=40.7636197,
        lng=-73.9744388,
        alias='Bergdorf Goodman',
        is_depot=True,
        time=0
    )
    address.add_address(
        address='717 5th Ave New York, NY 10022',
        lat=40.7669692,
        lng=-73.9693864,
        alias='Giorgio Armani',
        time=60
    )
    address.add_address(
        address='888 Madison Ave New York, NY 10014',
        lat=40.7715154,
        lng=-73.9669241,
        alias='Ralph Lauren Women\'s and Home',
        time=60
    )
    address.add_address(
        address='1011 Madison Ave New York, NY 10075',
        lat=40.7772129,
        lng=-73.9669,
        alias='Yigal Azrou\u00ebl',
        time=60
    )
    address.add_address(
        address='440 Columbus Ave New York, NY 10024',
        lat=40.7808364,
        lng=-73.9732729,
        alias='Frank Stella Clothier',
        time=60
    )
    address.add_address(
        address='324 Columbus Ave #1 New York, NY 10023',
        lat=40.7803123,
        lng=-73.9793079,
        alias='Liana',
        time=60
    )
    address.add_address(
        address='110 W End Ave New York, NY 10023',
        lat=40.7753077,
        lng=-73.9861529,
        alias='Toga Bike Shop',
        time=60
    )
    address.add_address(
        address='555 W 57th St New York, NY 10019',
        lat=40.7718005,
        lng=-73.9897716,
        alias='BMW of Manhattan',
        time=60
    )
    address.add_address(
        address='57 W 57th St New York, NY 10019',
        lat=40.7558695,
        lng=-73.9862019,
        alias='Verizon Wireless',
        time=60
    )

    response = r4m.run_optimization()
    print("Optimization Problem ID: {}".format(response.get("optimization_problem_id")))
    for a in response.get("addresses", []):
        print('{} - {} - {}'.format(a.get("sequence_no"), a.get("alias"), a.get("address")))
