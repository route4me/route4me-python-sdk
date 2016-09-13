import json

from .base import Base
from .exceptions import ParamValueException
from .utils import json2obj


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
            self.response = self.api._request_get(self.api.file_upload_preview_url(),
                                                  kwargs)
            return self.response.content
        else:
            raise ParamValueException('params', 'Params are not complete')

    def upload_file(self, **kwargs):
        """
        Upload File Preview using POST request
        :return: API response
        :raise: ParamValueException if required params are not present.

        """
        kwargs.update({'api_key': self.params['api_key'], })
        if self.check_required_params(kwargs, ['files', 'format',]):
            self.response = self.api._request_post(self.api.file_upload_url(),
                                                  kwargs, files=kwargs.pop('files'))
            return self.response.content
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
            self.response = self.api._request_post(self.api.file_upload_geocode_url(),
                                                  kwargs, files=kwargs.pop('files'))
            return self.response.content
        else:
            raise ParamValueException('params', 'Params are not complete')
