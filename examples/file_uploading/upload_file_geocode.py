from route4me import Route4Me

KEY = "11111111111111111111111111111111"


def main():
    route4me = Route4Me(KEY)
    file_uploading = route4me.file_uploading
    upload_id = 'b2130b5fc36ae1109ef63b6db73781f6'
    filename = '10-Stops-MultiDepotSmall.csv'
    upload_file = open(filename, 'rb')
    files = {'strFilename': upload_file}
    response = file_uploading.upload_file_geocode(strUploadID=upload_id,
                                                  files=files)
    print(response)


if __name__ == '__main__':
    main()
