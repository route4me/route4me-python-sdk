from route4me import Route4Me

KEY = "11111111111111111111111111111111"


def main():
    route4me = Route4Me(KEY)
    members = route4me.members
    data = {
        "member_id": 777777,
        "session_guid": "454563",
        "device_id": "54564",
        "device_type": "ipad",
        "subscription_name": "IPAD_MONTHLY",
        "token": "4/P7q7W91a-oMsCeLvIaQm6bTrgtp7",
        "payload": "APA91bHun4MxP5egoKMwt2KZFBaFUH-1RYqx",
        "format": "json",
    }
    response = members.app_purchase_user_license(**data)
    if hasattr(response, 'errors'):
        print('. '.join(response.errors))
    else:
        print(response)


if __name__ == '__main__':
    main()
