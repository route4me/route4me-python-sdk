# -*- coding: utf-8 -*-
# codebeat:disable[SIMILARITY]
import os

from route4me import Route4Me

KEY = "11111111111111111111111111111111"


def main():
    route4me = Route4Me(KEY)
    file_uploading = route4me.file_uploading
    file_path = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(file_path, '10-Stops-MultiDepotSmall.csv')
    upload_file = open(filename, 'rb')
    files = {'strFilename': upload_file}
    response = file_uploading.upload_file(files=files, format='json')
    print(response)


if __name__ == '__main__':
    main()
# codebeat:enable[SIMILARITY]
