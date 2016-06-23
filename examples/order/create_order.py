#!/usr/bin/python

from route4me import Route4Me

KEY = "11111111111111111111111111111111"


def main():
    route4me = Route4Me(KEY)
    order = route4me.order
    data = {'address_1': '106 Fulton St, Farmingdale, NY 11735, USA',
            'cached_lat': 40.730730,
            'cached_lng': -73.459283,
            'address_alias': 'BK Restaurant #: 17871',
            'EXT_FIELD_phone': '(212) 566-5132',
            'day_scheduled_for_YYMMDD': '2016-07-01',
            'EXT_FIELD_custom_data': {'url': "http://www.bk.com/restaurants/ny/new-york/106-fulton-st-17871.html"
                                      }
            }
    response = order.create_order(**data)
    print 'Member ID:\t{0}'.format(response.get('member_id'))
    print 'Order ID:\t{0}'.format(response.get('order_id'))
    print 'Order Status ID:\t{0}'.format(response.get('order_status_id'))
    print 'In Route Count:\t{0}'.format(response.get('in_route_count'))
    print 'Day Added:\t{0}'.format(response.get('day_added_YYMMDD'))
    print 'Is Pending:\t{0}'.format(response.get('is_pending'))
    print 'Is Accepted:\t{0}'.format(response.get('is_accepted'))
    print 'Is Started:\t{0}'.format(response.get('is_started'))
    print 'Is Validated:\t{0}'.format(response.get('is_validated'))
    print 'Is Completed:\t{0}'.format(response.get('is_completed'))

if __name__ == '__main__':
    main()
