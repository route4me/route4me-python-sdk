# -*- coding: utf-8 -*-

DRIVER_VERSION = 'route4me-python-driver-0.0.1'


class APIException(Exception):
    """
    Handle API Exceptions
    """

    def __init__(self, status_code, response, url):
        self.status_code = status_code
        self.response = response
        self.url = url
        exception = {'http_status_code': status_code,
                     'response': response,
                     'url': url,
                     'driver_version': DRIVER_VERSION}
        Exception.__init__(self, exception)

    def get_status_code(self):
        """
        Status code
        :return:
        """
        return self.status_code

    def get_response(self):
        """
        Return response
        :return:
        """
        return self.response


class ParamValueException(Exception):
    """
    Handle Params exceptions
    """

    def __init__(self, param, msg):
        self.param = param
        self.msg = msg
        exception = {'param': param,
                     'msg': msg, }
        Exception.__init__(self, exception)

    def get_msg(self):
        """
        Message from exception
        :return:
        """
        return self.msg
