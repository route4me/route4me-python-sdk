#!/usr/bin/python

from route4me import Route4Me

KEY = "11111111111111111111111111111111"


def main():
    route4me = Route4Me(KEY)
    response = route4me.get_users()
    if hasattr(response, 'errors'):
        print '. '.join(response.errors)
    else:
        for i, member in enumerate(response):
            print 'Member #{}'.format(i+1)
            print '\tName: {0}, {1}'.format(member.member_first_name, member.member_last_name)
            print '\tEmail: {}'.format(member.member_email)

if __name__ == '__main__':
    main()
