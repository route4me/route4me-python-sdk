# -*- coding: utf-8 -*-
# codebeat:disable[SIMILARITY]

import argparse
import os
from route4me import Route4Me


def main(api_key):
    route4me = Route4Me(api_key)
    file_uploading = route4me.file_uploading
    file_path = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(file_path, '4 addresses linked 2 New Filters.xlsx')
    upload_file = open(filename, 'rb')
    files = {'strFilename': upload_file}
    response = file_uploading.upload_file(files=files, format='json')
    print(response)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Upload XLSX File')
    parser.add_argument('--api_key', dest='api_key', help='Route4Me API KEY',
                        type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)

# codebeat:enable[SIMILARITY]
