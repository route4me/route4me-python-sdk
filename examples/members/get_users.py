from route4me import Route4Me

KEY = "11111111111111111111111111111111"


def main():
    route4me = Route4Me(KEY)
    members = route4me.members
    response = members.get_users(limit=5, offset=0)
    if 'errors' in list(response.keys()):
        print '. '.join(response.get('errors'))
    else:
        for i, member in enumerate(response):
            print('Member #{}'.format(i + 1))
            print('\tName: {0}, {1}'.format(
                member.get('member_first_name'),
                member.get('member_last_name')
            ))
            print('\tEmail: {}'.format(member.get('member_email')))


if __name__ == '__main__':
    main()
