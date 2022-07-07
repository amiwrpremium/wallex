import typing as t
import json

from requests import Response
from aiohttp import ClientResponse


class APIException(Exception):
    def __init__(self, response: t.Union[Response, ClientResponse], status_code: int, text: str):
        self.code = 0
        try:
            json_res = json.loads(text)
        except ValueError:
            self.message = 'Invalid JSON error message from Wallex: {}'.format(response.text)
        else:
            self.code = json_res['code']
            self.message = json_res['message']
            self.result = json_res['result']

        self.status_code = status_code
        self.response = response
        self.request = getattr(response, 'request', None)

    def __str__(self):  # pragma: no cover
        return 'APIError(code=%s): %s | %s' % (self.code, self.message, self.result)


class RequestException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return 'RequestException: %s' % self.message


class OrderException(Exception):
    def __init__(self, field: str, message: str):
        self.field = field
        self.message = message

    def __str__(self):
        return 'OrderException(code=%s): %s' % (self.field, self.message)
