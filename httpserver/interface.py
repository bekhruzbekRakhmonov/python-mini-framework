from collections.abc import MutableMapping
from .errors import InterfaceError


class Interface:
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    @property
    def is_valid(self) -> bool:
        annotated_types = self.__annotations__
        for key in annotated_types.keys():
            val = self.kwargs.get(key)
            if val is None:
                return InterfaceError(f"'{key}' is required")
            if not isinstance(val, annotated_types[key]):
                return InterfaceError(f"'{key}' got invalid type")
        return True
