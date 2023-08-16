from jinja2 import Environment as BaseEnvironment
from jinja2 import FileSystemLoader
from pathlib import Path
from typing import (
    Any,
    Dict,
    Optional,
    Union,
    TYPE_CHECKING
)
import os
from .. import settings
from .ext import StaticExtension

if TYPE_CHECKING:
    from jinja2 import BaseLoader, Template
    from .request import Request


class Environment(BaseEnvironment):
    def __init__(self, **options: Any) -> None:
        super(Environment, self).__init__(**options)


def render(request: "Request", template_name: str, context: Dict[str, Any]) -> str:
    print(settings.TEMPLATE_DIRS)
    loader = FileSystemLoader(searchpath=settings.TEMPLATE_DIRS)
    env = Environment(loader=loader, extensions=[StaticExtension])
    template = env.get_template(template_name)
    context["request"] = request
    return template.render(context)
