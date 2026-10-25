"""Request-level tests for :meth:`route4me.file_uploading.FileUploading.upload_addresses_to_temporary_storage`.

The older :class:`~route4me.file_uploading.FileUploading` methods are tested in
``test_telematics_files.py``.
"""

import json

import responses

from route4me.api_endpoints import FAST_GEOCODER

ROWS = [{"ADDRESS": "1 Example Way", "CITY": "Springfield", "STATE": "IL", "ZIP": "62701"}]


class TestUploadAddressesToTemporaryStorage:
    def test_posts_the_rows_as_json(self, client, mocked, last_request, query_of):
        reply = {"optimization_problem_id": "STORAGE-1", "address_count": 1, "status": True}
        mocked.add(responses.POST, FAST_GEOCODER, json=reply, status=200)

        assert client.file_uploading.upload_addresses_to_temporary_storage(ROWS) == reply
        assert last_request().method == "POST"
        assert query_of(last_request()) == {"api_key": client.key}
        assert json.loads(last_request().body) == {"rows": ROWS}

    def test_an_api_error_is_returned_as_a_dict(self, client, mocked):
        mocked.add(responses.POST, FAST_GEOCODER, json={"errors": ["Please use post"]}, status=409)

        assert client.file_uploading.upload_addresses_to_temporary_storage(ROWS) == {"errors": ["Please use post"]}
