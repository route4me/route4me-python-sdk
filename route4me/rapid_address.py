import json

from .base import Base
from .exceptions import ParamValueException
from .utils import json2obj


class RapidAddress(Base):
    """
    Rapid Address is a service to get Street Addresses given
    Street name or Zip code
    """

    def __init__(self, api):
        """
        Address Instance
        :param api:
        :return:
        """
        Base.__init__(self, api)

    def get_street_data(self, **kwargs):
        """
        Get Street Data
        :param kwargs:
        :return: API response content
        """
        kwargs.update({'api_key': self.params['api_key'], })
        response = self.api._request_get(self.api.rapid_address_url(), kwargs)
        try:
            return json.loads(response.content)
        except ValueError:
            return response.content

    def get_street_data_zip(self, **kwargs):
        """
        Get Street Data Given Zipcode
        :param kwargs:
        :return: API response content
        """
        kwargs.update({'api_key': self.params['api_key'], })
        url = self.api.rapid_address_zip_url()
        if self.check_required_params(kwargs, ['zipcode', 'api_key', ]):
            url = '{0}{1}/'.format(url, kwargs.pop('zipcode'))
            if 'offset' in kwargs.keys() and 'limit' in kwargs.keys():
                url = '{0}{1}/{2}/'.format(url, kwargs.pop('offset'), kwargs.pop('limit'))
            response = self.api._request_get(url, kwargs)
            try:
                return json.loads(response.content)
            except ValueError:
                return response.content
        else:
            raise ParamValueException('params', 'Params are not complete')

    def get_street_data_service(self, **kwargs):
        """
        Get Street Data Given Zipcode and House Number
        :param kwargs:
        :return: API response content
        """
        kwargs.update({'api_key': self.params['api_key'], })
        url = self.api.rapid_address_service_url()
        if self.check_required_params(kwargs, ['zipcode', 'api_key', 'housenumber', ]):
            url = '{0}{1}/{2}/'.format(url, kwargs.pop('zipcode'), kwargs.pop('housenumber'))
            if 'offset' in kwargs.keys() and 'limit' in kwargs.keys():
                url = '{0}{1}/{2}/'.format(url, kwargs.pop('offset'), kwargs.pop('limit'))
            response = self.api._request_get(url, kwargs)
            try:
                return json.loads(response.content)
            except ValueError:
                return response.content
        else:
            raise ParamValueException('params', 'Params are not complete')
