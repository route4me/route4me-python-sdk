# -*- coding: utf-8 -*-

from .api_endpoints import FILE_UPLOAD_HOST, \
    FILE_UPLOAD_PREVIEW_HOST, FILE_UPLOAD_GEOCODE_HOST
from .base import Base
from .exceptions import ParamValueException, APIException


class FileUploading(Base):
    """
    File Uploading is a service to upload data files
    """

    def __init__(self, api):
        """
        FileUploading Instance
        :param api:
        :return:
        """
        Base.__init__(self, api)

    def get_file_preview(self, **kwargs):
        """
        Get File Preview using GET request
        :return: API response
        :raise: ParamValueException if required params are not present.

        """
        kwargs.update({'api_key': self.params['api_key'], })
        if self.check_required_params(kwargs, ['strUploadID', 'format']):
            try:
                self.response = self.api._make_request(FILE_UPLOAD_PREVIEW_HOST,
                                                       kwargs,
                                                       self.api._request_get)
                return self.response.content
            except APIException as e:
                return e.to_dict()
        else:
            raise ParamValueException('params', 'Params are not complete')

    def upload_file(self, **kwargs):
        """
        Upload File Preview using POST request
        :return: API response
        :raise: ParamValueException if required params are not present.

        """
        kwargs.update({'api_key': self.params['api_key'], })
        if self.check_required_params(kwargs, ['files',
                                               'format', ]):
            try:
                self.response = self.api._make_request(FILE_UPLOAD_HOST,
                                                       kwargs,
                                                       self.api._request_post,
                                                       files=kwargs.pop('files'))
                return self.response.content
            except APIException as e:
                return e.to_dict()
        else:
            raise ParamValueException('params', 'Params are not complete')

    def upload_file_geocode(self, **kwargs):
        """
        Upload File Geocode using POST request
        :return: API response
        :raise: ParamValueException if required params are not present.

        """
        kwargs.update({'api_key': self.params['api_key'], })
        if self.check_required_params(kwargs, ['strUploadID', 'files', ]):
            try:
                self.response = self.api._make_request(FILE_UPLOAD_GEOCODE_HOST,
                                                       kwargs,
                                                       self.api._request_post,
                                                       files=kwargs.pop('files'))
                return self.response.content
            except APIException as e:
                return e.to_dict()
        else:
            raise ParamValueException('params', 'Params are not complete')
