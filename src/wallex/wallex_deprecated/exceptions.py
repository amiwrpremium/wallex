import typing as t
from requests import Response


__all__ = [
    'WallexExceptions',
    'RequestsExceptions',
    'RequestTimeout',
    'TokenException',
    'InvalidResponse',
    'StatusCodeError',
    'JSONDecodingError',
    'InvalidInputs',
    'WebsocketExceptions',
    'WebsocketNotConnected'
]


class WallexExceptions(Exception):
    def __init__(
            self, func_name: str, message: t.Union[str, t.Type[Exception], Exception], *args, **kwargs
    ):
        """
        Base exception class for Bitpin.

        :param func_name: function name that raise exception
        :type func_name: str

        :param message: message of exception
        :type message: str | Exception

        :param args: args of exception
        :type args: t.Any

        :param kwargs: kwargs of exception
        :type kwargs: t.Any

        :return: None
        :rtype: None
        """

        self.func_name = func_name
        self.message = str(message)
        self.f_args = args
        self.f_kwargs = kwargs
        super().__init__(self.message)

    def __str__(self):
        __str = f'[{self.func_name}] -> {self.message}'

        if self.f_args and len(self.f_args) > 0:
            __str += f' | Args: {self.f_args}'
        if self.f_kwargs:
            __str += f' | Kwargs: {self.f_kwargs}'

        return __str


class RequestsExceptions(WallexExceptions):
    """ Exception class for requests error. """


class RequestTimeout(RequestsExceptions):
    """ Exception class for requests timeout error. """


class TokenException(RequestsExceptions):
    """ Exception class for invalid token error. """


class ProcessExceptions(WallexExceptions):
    """ Exception class for process error. """

    def __init__(self, func_name: str, message: str, response: Response, *args, **kwargs):
        self.response = response
        msg = f'{message} || {response.text}'
        super().__init__(func_name, msg, *args, **kwargs)


class StatusCodeError(ProcessExceptions):
    """ Exception class for status code error. """


class JSONDecodingError(ProcessExceptions):
    """ Exception class for json decode error. """


class InvalidResponse(ProcessExceptions):
    """ Exception class for invalid response error. """


class InvalidInputs(WallexExceptions):
    """ Exception class for invalid requested data error. """


class WebsocketExceptions(WallexExceptions):
    """ Exception class for websocket error. """


class WebsocketNotConnected(WebsocketExceptions):
    """ Exception class for websocket not connected error. """
