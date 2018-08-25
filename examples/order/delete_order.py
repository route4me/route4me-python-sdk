# -*- coding: utf-8 -*-
# codebeat:disable[ABC]

from route4me import Route4Me

API_KEY = "11111111111111111111111111111111"


def main():
    route4me = Route4Me(API_KEY)
    order = route4me.order
    url = "http://www.bk.com/restaurants/ny/new-york/106-fulton-st-17871.html"
    data = {
        'address_1': '106 Fulton St, Farmingdale, NY 11735, USA',
        'cached_lat': 40.730730,
        'cached_lng': -73.459283,
        'address_alias': 'BK Restaurant #: 17871',
        'EXT_FIELD_phone': '(212) 566-5132',
        'day_scheduled_for_YYMMDD': '2016-07-01',
        'EXT_FIELD_custom_data': {
            'url': url
        }
    }
    response = order.create_order(**data)
    if isinstance(response, dict) and 'errors' in response.keys():
        print('. '.join(response['errors']))
    else:
        print('Member ID:\t{0}'.format(response.get('member_id')))
        print('Order ID:\t{0}'.format(response.get('order_id')))
        print('Order Status ID:\t{0}'.format(response.get('order_status_id')))
        print('In Route Count:\t{0}'.format(response.get('in_route_count')))
        print('Day Added:\t{0}'.format(response.get('day_added_YYMMDD')))
        print('Is Pending:\t{0}'.format(response.get('is_pending')))
        print('Is Accepted:\t{0}'.format(response.get('is_accepted')))
        print('Is Started:\t{0}'.format(response.get('is_started')))
        print('Is Validated:\t{0}'.format(response.get('is_validated')))
        print('Is Completed:\t{0}'.format(response.get('is_completed')))
        print('********************************************************')
        print('Deleting')
        print('********************************************************')
        order_id = response.get('order_id')
        if order_id:
            data = {'order_ids': [order_id]}
            response = order.delete_order(**data)
            print(response)
        else:
            print('Error Getting Order')


if __name__ == '__main__':
    main()
# codebeat:enable[ABC]
