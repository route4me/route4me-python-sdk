"""Geocode the addresses of an uploaded file.

Calls :meth:`FileUploading.upload_file_geocode
<route4me.file_uploading.FileUploading.upload_file_geocode>` with the upload ID and
``10-Stops-MultiDepotSmall.csv``, next to this script, which sends
``POST /actions/upload/csv-xls-geocode.php`` with ``strUploadID`` in the query and the file as a
multipart upload, and prints the raw reply.

Run it with::

    python examples/file_uploading/upload_file_geocode.py --api_key <your key> --upload_id <upload ID>
"""

import argparse
import os

from route4me import Route4Me


def main(api_key, upload_id):
    """Geocode an uploaded file and print the reply.

    :param api_key: Route4Me API key.
    :param upload_id: ID of the upload.
    """
    route4me = Route4Me(api_key)
    file_uploading = route4me.file_uploading
    file_path = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(file_path, "10-Stops-MultiDepotSmall.csv")
    with open(filename, "rb") as upload_file:
        response = file_uploading.upload_file_geocode(strUploadID=upload_id, files={"strFilename": upload_file})
    print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upload File to Geocode")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument("--upload_id", dest="upload_id", help="ID of an upload, from upload_file.py", required=True)
    args = parser.parse_args()
    main(args.api_key, args.upload_id)
