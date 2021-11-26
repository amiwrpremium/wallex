from typing import Union


class WallexExceptions(BaseException):
    def __init__(self, func_name: str, message: Union[str, Exception], args: dict):
        self.func_name = func_name
        self.message = str(message)
        self._args = args
        super().__init__(self.message)

    def __str__(self):
        return f'"{self.func_name}" -> {self.message} | {str(self._args)}'


class RequestsExceptions(WallexExceptions):
    pass


class StatusCodeError(WallexExceptions):
    def __init__(self, func_name: str, status_code: int, message: Union[str, Exception], args: dict):
        self.func_name = func_name
        self.status_code = status_code
        self.message = message
        self._args = args
        super().__init__(func_name, message, args)

    def __str__(self):
        return f'{self.func_name} | {self.status_code} -> {self.message} | {str(self._args)}'


class JsonDecodingError(WallexExceptions):
    def __init__(self, func_name: str, message: Union[str, Exception], args: dict):
        self.func_name = func_name
        self.message = message
        self._args = args
        super().__init__(func_name, message, args)

    def __str__(self):
        return f'{self.func_name} -> {self.message} | {str(self._args)}'


class InvalidResponse(WallexExceptions):
    def __init__(self, func_name: str, message: Union[str, Exception], args: dict):
        self.func_name = func_name
        self.message = message
        self._args = args
        super().__init__(func_name, message, args)

    def __str__(self):
        return f'{self.func_name} -> {self.message} | {str(self._args)}'
