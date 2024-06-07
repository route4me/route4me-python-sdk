# -*- coding: utf-8 -*-

import argparse
import os
from route4me import Route4Me


def main(api_key):
    route4me = Route4Me(api_key)
    file_uploading = route4me.file_uploading
    upload_id = 'b2130b5fc36ae1109ef63b6db73781f6'

    file_path = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(file_path, '10-Stops-MultiDepotSmall.csv')
    upload_file = open(filename, 'rb')
    files = {'strFilename': upload_file}
    response = file_uploading.upload_file_geocode(strUploadID=upload_id,
                                                  files=files)
    print(response)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Upload File to Geocode')
    parser.add_argument('--api_key', dest='api_key', help='Route4Me API KEY',
                        type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
