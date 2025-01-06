# views/__init__.py
from .personal_view import RegistroPersonalView
from .main_view import MainView
from .busqueda_view import BusquedaView

__all__ = [
    'LoginView',
    'MainView',
    'RegistroPersonalView',
    'BusquedaView'
]