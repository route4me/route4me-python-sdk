from route4me import Route4Me

KEY = "11111111111111111111111111111111"


def main():
    route4me = Route4Me(KEY)
    members = route4me.members
    data = {
        "device_id": "546546516",
        "device_type": "ipad",
        "format": "json",
    }
    response = members.verify_device_license(**data)
    if hasattr(response, 'errors'):
        print('. '.join(response.errors))
    else:
        print(response)


if __name__ == '__main__':
    main()
