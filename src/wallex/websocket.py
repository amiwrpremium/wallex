import typing as t


import socketio
import engineio


from .exceptions import WebsocketNotConnected
from ._package_data import __version__, __author__


if socketio.__version__ < '4.0.0' or socketio.__version__ >= '5.0.0':
    raise RuntimeError('socketio version should be > 4.0.0 and <= 5.0.0')
if engineio.__version__ < '2.0.0' or engineio.__version__ >= '3.0.0':
    raise RuntimeError('engineio version should be > 2.0.0 and <= 3.0.0')


class WallexWebsocket:
    """
    Wallex Websocket class.
    """

    def __init__(self, url: str = 'https://api.wallex.ir/socket.io',
                 socketio_params: t.Optional[t.Dict[str, t.Any]] = None,
                 debug: t.Optional[bool] = False):
        """
        Wallex Websocket class constructor.

        :param url: Websocket URL
        :type url: str

        :param socketio_params: SocketIO parameters (optional)
        :type socketio_params: t.Dict[str, t.Any]

        :param debug: Enable debug mode (optional)
        :type debug: t.Optional[bool]

        :return: Wallex Websocket class instance
        :rtype: WallexWebsocket
        """
        self._sio: socketio.Client = socketio.Client(**socketio_params or {})
        self._url: str = url
        self._debug: bool = debug

        self._is_connected: bool = False

    def __exc_if_not_connected(self, f_name: str):
        """
        Raise exception if not connected.

        :param f_name: Function name
        :type f_name: str

        :return: None
        """

        if not self._is_connected:
            raise WebsocketNotConnected(f_name, 'Websocket is not connected')

    def __debug_print(self, msg: str, *args, **kwargs):
        """
        Print debug message if debug mode is enabled.

        :param msg: Message to print
        :type msg: str

        :param args: Arguments to pass to print
        :type args: t.Any

        :param kwargs: Keyword arguments to pass to print
        :type kwargs: t.Any

        :return: None
        """

        message = str(msg)

        if args and len(args) > 0:
            message += f" | {args}"

        if kwargs and len(kwargs) > 0:
            message += f" | {kwargs}"

        if self._debug:
            print(message)

    def connect(self, url: t.Optional[str] = None, params: t.Optional[t.Dict[str, t.Any]] = None):
        """
        Connect to a websocket.

        :param url: Websocket URL (optional)
        :type url: t.Optional[str]

        :param params: SocketIO parameters (optional)
        :type params: t.Optional[t.Dict[str, t.Any]]

        :return: None
        """

        _url = url or self._url
        self._sio.connect(_url, **params or {})
        self._is_connected = True
        self.__debug_print('Connection established')

    def disconnect(self):
        """
        Disconnect from a websocket.

        :return: None
        """

        self.__exc_if_not_connected('disconnect')
        self._sio.disconnect()
        self._is_connected = False
        self.__debug_print('Connection closed')

    def subscribe(self, channel: str):
        """
        Subscribe to a channel

        :param channel: Channel name
        :type channel: str

        :return: None
        """

        self.__exc_if_not_connected('subscribe')
        self.emit('subscribe', data={"channel": channel})
        self.__debug_print(f'Subscribed to channel: {channel}')

    def unsubscribe(self, channel: str):
        """
        Unsubscribe from a channel

        :param channel: Channel name
        :type channel: str

        :return: None
        """

        self.__exc_if_not_connected('unsubscribe')
        self.emit('unsubscribe', data={"channel": channel})
        self.__debug_print(f'Unsubscribed from channel: {channel}')

    def wait(self):
        """
        Wait for a message.

        :return: None
        """

        self.__exc_if_not_connected('wait')
        self._sio.wait()

    def emit(self, event: str, data: t.Dict[str, t.Any]):
        """
        Emit an event.

        :param event: Event name
        :type event: str

        :param data: Event data
        :type data: t.Dict[str, t.Any]

        :return: None
        """

        self.__exc_if_not_connected('emit')
        self._sio.emit(event, data)
        self.__debug_print(f'Emitted event', event=event, data=data)

    def on(self, event: str, callback: t.Callable[[str, t.Dict[str, t.Any]], None]):
        """
        Register a callback for an event.

        :param event: Event name
        :type event: str

        :param callback: Callback function
        :type callback: t.Callable[[str, t.Dict[str, t.Any]], None]

        :return: None
        """

        self.__exc_if_not_connected('on')
        self._sio.on(event, callback)
        self.__debug_print(f'Registered callback for event', event=event)

    def on_connect(self, callback: t.Callable[[], None]):
        """
        Register a callback for connection.

        :param callback: Callback function
        :type callback: t.Callable[[], None]

        :return: None
        """

        self.__exc_if_not_connected('on_connect')
        self.on('connect', callback)

    def on_disconnect(self, callback: t.Callable[[], None]):
        """
        Register a callback for disconnection.

        :param callback: Callback function
        :type callback: t.Callable[[], None]

        :return: None
        """

        self.__exc_if_not_connected('on_disconnect')
        self.on('disconnect', callback)

    def on_error(self, callback: t.Callable[[str, t.Dict[str, t.Any]], None]):
        """
        Register a callback for error.

        :param callback: Callback function
        :type callback: t.Callable[[str, t.Dict[str, t.Any]], None]

        :return: None
        """

        self.__exc_if_not_connected('on_error')
        self.on('error', callback)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    def __str__(self):
        return f'Wallex Websocket Client, By {__author__}, Version {__version__}'

    def __repr__(self):
        return f'Wallex Websocket API Client, By {__author__}, Version {__version__}'
