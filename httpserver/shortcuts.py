from http import HTTPStatus as status
from .router import router
from .response import HttpResponse, HttpResponseRedirect
from .template import template

import typing

if typing.TYPE_CHECKING:
    from .request import Request

HOST = "http://127.0.0.1:8000"


def redirect(redirect_to: str, args: tuple) -> HttpResponseRedirect:
    return HttpResponseRedirect(redirect_to, args)


def render_template(request: "Request", template_name: str, context: dict = {}) -> HttpResponse:
    response_text = template.render(request, template_name, context)
    return HttpResponse(response_text=response_text)
