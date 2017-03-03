from route4me import Route4Me

KEY = "11111111111111111111111111111111"


def main():
    route4me = Route4Me(KEY)
    members = route4me.members
    data = {
        "session_guid": "4552222222",
        "member_id": "787544566",
        "format": "json"
    }
    response = members.validate_session(**data)
    if hasattr(response, 'errors'):
        print('. '.join(response.errors))
    else:
        print(response)


if __name__ == '__main__':
    main()
