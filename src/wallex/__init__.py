from .main import Wallex
from .websocket import WallexWebsocket

from . import exceptions

from ._deprecated import Wallex as WallexDeprecated

from ._package_data import __version__


__all__ = [
    'Wallex',
    'WallexWebsocket',
    'exceptions',
]
