from .interface import Interface

class UserInterface(Interface):
    name: str
    password: int

class CustomUserInterface(Interface):
    username: str
    password: str
    name: int