from . import wallex_deprecated

from .clients import Client, AsyncClient

from ._package_data import __version__


__all__ = [
    'Client',
    'AsyncClient',
]
