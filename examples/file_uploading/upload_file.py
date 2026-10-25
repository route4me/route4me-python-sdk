"""Upload a CSV file of addresses.

Calls :meth:`FileUploading.upload_file <route4me.file_uploading.FileUploading.upload_file>` with
``10-Stops-MultiDepotSmall.csv``, next to this script, as ``strFilename`` and ``format="json"``, which
sends ``POST /actions/upload/upload.php`` as a multipart upload. Prints the raw reply, which identifies
the upload for get_file_preview.py and upload_file_geocode.py.

Run it with::

    python examples/file_uploading/upload_file.py --api_key <your key>
"""

import argparse
import os

from route4me import Route4Me


def main(api_key):
    """Upload the sample CSV file and print the reply.

    :param api_key: Route4Me API key.
    """
    route4me = Route4Me(api_key)
    file_uploading = route4me.file_uploading
    file_path = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(file_path, "10-Stops-MultiDepotSmall.csv")
    with open(filename, "rb") as upload_file:
        response = file_uploading.upload_file(files={"strFilename": upload_file}, format="json")
    print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upload a File")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    args = parser.parse_args()
    main(args.api_key)
