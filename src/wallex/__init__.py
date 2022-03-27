from .main import Wallex
from . import exceptions

from ._deprecated import Wallex as WallexDeprecated

from ._package_data import __version__


__all__ = [
    'Wallex',
    'exceptions',
]
