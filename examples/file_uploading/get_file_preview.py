"""Preview the content of an uploaded file.

Calls :meth:`FileUploading.get_file_preview <route4me.file_uploading.FileUploading.get_file_preview>`
with the upload ID and ``format="json"``, which sends ``GET /actions/upload/csv-xls-preview.php`` with
``strUploadID``, and prints the raw reply. upload_file.py prints the reply of a new upload, which
identifies it.

Run it with::

    python examples/file_uploading/get_file_preview.py --api_key <your key> --upload_id <upload ID>
"""

import argparse

from route4me import Route4Me


def main(api_key, upload_id):
    """Print the preview of an uploaded file.

    :param api_key: Route4Me API key.
    :param upload_id: ID of the upload.
    """
    route4me = Route4Me(api_key)
    file_uploading = route4me.file_uploading
    response = file_uploading.get_file_preview(format="json", strUploadID=upload_id)
    print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get File Preview")
    parser.add_argument("--api_key", dest="api_key", help="Route4Me API KEY", type=str, required=True)
    parser.add_argument("--upload_id", dest="upload_id", help="ID of an upload, from upload_file.py", required=True)
    args = parser.parse_args()
    main(args.api_key, args.upload_id)
