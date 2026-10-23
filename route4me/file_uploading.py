"""The :class:`FileUploading` resource: upload CSV and XLS(X) files of addresses, preview and geocode them."""

from .api_endpoints import FAST_GEOCODER, FILE_UPLOAD_GEOCODE_HOST, FILE_UPLOAD_HOST, FILE_UPLOAD_PREVIEW_HOST
from .base import Base
from .exceptions import APIException, ParamValueException


class FileUploading(Base):
    """File uploading: send data files of addresses to Route4Me.

    Use it as ``route4me.file_uploading``. Unless stated otherwise, a method
    returns the raw response body (``bytes``), or on an API error the
    ``{"errors": ...}`` dict from :meth:`APIException.to_dict
    <route4me.exceptions.APIException.to_dict>` instead of raising.
    """

    def __init__(self, api):
        """Create the resource.

        :param api: the :class:`~route4me.api.Route4Me` client.
        """
        Base.__init__(self, api)

    def get_file_preview(self, **kwargs):
        """Preview the content of an uploaded file.

        Sends ``GET /actions/upload/csv-xls-preview.php``.

        :param kwargs: query parameters. Required: ``strUploadID``, the ID of
            the upload, and ``format``, e.g. ``"json"``.
        :return: the raw response body (``bytes``), or the ``{"errors": ...}``
            dict on an API error.
        :raise ParamValueException: when a required parameter is missing.
        """
        kwargs.update(
            {
                "api_key": self.params["api_key"],
            }
        )
        if self.check_required_params(kwargs, ["strUploadID", "format"]):
            try:
                self.response = self._request(FILE_UPLOAD_PREVIEW_HOST, kwargs, "get")
                return self.response.content
            except APIException as e:
                return e.to_dict()
        else:
            raise ParamValueException("params", "Params are not complete")

    def upload_file(self, **kwargs):
        """Upload a file.

        Sends ``POST /actions/upload/upload.php`` with ``files`` as a multipart
        upload and the other keywords in the query.

        :param kwargs: required: ``files``, a ``requests`` files mapping such
            as ``{"strFilename": open(path, "rb")}``, and ``format``, e.g.
            ``"json"``.
        :return: the raw response body (``bytes``), which identifies the
            upload, or the ``{"errors": ...}`` dict on an API error.
        :raise ParamValueException: when a required parameter is missing.
        """
        kwargs.update(
            {
                "api_key": self.params["api_key"],
            }
        )
        if self.check_required_params(
            kwargs,
            [
                "files",
                "format",
            ],
        ):
            try:
                self.response = self._request(FILE_UPLOAD_HOST, kwargs, "post", files=kwargs.pop("files"))
                return self.response.content
            except APIException as e:
                return e.to_dict()
        else:
            raise ParamValueException("params", "Params are not complete")

    def upload_file_geocode(self, **kwargs):
        """Geocode the addresses of an uploaded file.

        Sends ``POST /actions/upload/csv-xls-geocode.php`` with ``files`` as a
        multipart upload and the other keywords in the query.

        :param kwargs: required: ``strUploadID``, the ID of the upload, and
            ``files``, a ``requests`` files mapping such as
            ``{"strFilename": open(path, "rb")}``.
        :return: the raw response body (``bytes``), or the ``{"errors": ...}``
            dict on an API error.
        :raise ParamValueException: when a required parameter is missing.
        """
        kwargs.update(
            {
                "api_key": self.params["api_key"],
            }
        )
        if self.check_required_params(
            kwargs,
            [
                "strUploadID",
                "files",
            ],
        ):
            try:
                self.response = self._request(FILE_UPLOAD_GEOCODE_HOST, kwargs, "post", files=kwargs.pop("files"))
                return self.response.content
            except APIException as e:
                return e.to_dict()
        else:
            raise ParamValueException("params", "Params are not complete")

    def upload_addresses_to_temporary_storage(self, rows):
        """Upload addresses as JSON to temporary storage, for fast bulk geocoding.

        Sends ``POST /actions/upload/json-geocode.php`` with
        ``{"rows": rows}`` as the JSON body. The reply identifies the stored
        batch of addresses.

        :param rows: the addresses, a list of dicts with one key per column,
            e.g. ``{"ADDRESS": "1 Example Way", "CITY": "Springfield",
            "STATE": "IL", "ZIP": "62701"}``.
        :return: the decoded JSON reply, with ``optimization_problem_id``
            (the storage ID), ``temporary_addresses_storage_id``,
            ``address_count`` and ``status``, or the ``{"errors": ...}`` dict on
            an API error.

        .. versionadded:: 1.0.0
        """
        return self._call_api(FAST_GEOCODER, "post", {}, body={"rows": rows})
