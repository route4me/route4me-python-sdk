from route4me import Route4Me
from route4me.constants import *

KEY = "11111111111111111111111111111111"


def main():
    route4me = Route4Me(KEY)
    file_uploading = route4me.file_uploading
    upload_id = 'b2130b5fc36ae1109ef63b6db73781f6'
    response = file_uploading.get_file_preview(format='json', strUploadID=upload_id)
    print response


if __name__ == '__main__':
    main()
