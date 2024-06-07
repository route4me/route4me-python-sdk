# -*- coding: utf-8 -*-

import argparse

from route4me import Route4Me


def main(api_key):
    route4me = Route4Me(api_key)
    file_uploading = route4me.file_uploading
    upload_id = 'b2130b5fc36ae1109ef63b6db73781f6'
    response = file_uploading.get_file_preview(format='json',
                                               strUploadID=upload_id)
    print(response)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Get File Preview')
    parser.add_argument('--api_key', dest='api_key', help='Route4Me API KEY',
                        type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
