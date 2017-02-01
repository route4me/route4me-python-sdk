# codebeat:disable[SIMILARITY]
from route4me import Route4Me
from route4me.constants import *

KEY = "11111111111111111111111111111111"


def main():
    route4me = Route4Me(KEY)
    file_uploading = route4me.file_uploading
    filename = '10-Stops-MultiDepotSmall.csv'
    upload_file = open(filename, 'rb')
    files = {'strFilename': upload_file}
    response = file_uploading.upload_file(files=files, format='json')
    print response


if __name__ == '__main__':
    main()
# codebeat:enable[SIMILARITY]
