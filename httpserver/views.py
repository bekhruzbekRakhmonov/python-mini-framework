from http import HTTPStatus as status
from abc import ABC, abstractmethod
from .response import HttpResponse, BaseResponse
from .shortcuts import redirect, render_template
from .interfaces import UserInterface,CustomUserInterface
from .exceptions import ResponseException
from . import router

import typing

if typing.TYPE_CHECKING:
    from . import type as types
    from .request import Request


class BaseView:
    allowed_methods = ["GET","POST"]

    def get(self, request: "Request", **params) -> "types.Response":
        pass

    def post(self, request: "Request", **params) -> "types.Response":
        pass

    def check_method(self, request: "Request") -> bool:
        if request.method not in self.allowed_methods:
            return False
        return True

    def dispatch(self, request: "Request", **params) -> "types.Response":
        if not self.check_method(request):
            return HttpResponse(status=status.METHOD_NOT_ALLOWED,
                                response_text=f"{status.METHOD_NOT_ALLOWED} {status.METHOD_NOT_ALLOWED.phrase}")

        if request.method == "GET":
            return self.get(request, **params)
        elif request.method == "POST":
            return self.post(request, **params)

    def get_context_data(self, **kwargs):
        pass

    def __call__(self, request: "Request", **params) -> "types.Response":
        response = self.dispatch(request, **params)

        if not issubclass(response.__class__, BaseResponse):
            raise ResponseException(
                f"Response must be instance of '{str(BaseResponse)}'")

        return response


class View(BaseView):
    def get(self, request, **params):
        print("Class based View", params.get("id"))
        print(request.cookies)
        print(request.headers)
        return render_template(request, template_name="index.html")


def index(request, **params):
    print(request.headers)
    print(request.method)
    print("PARAMS", params)
    print("REQUEST", request.path)
    print("VALUES", request.values)

    response = HttpResponse(headers={"Content-Type": "text/html"},
                            status=status.OK, response_file="../frontend/index.html")

    # response.set_cookie(key="sessionid", value="40545464654", coded_value="1234")
    # return redirect("images",args=(2,))
    return render_template(request, "index.html", {"name": "Bexruz Raxmonov"})


@router.route(route_path="/myimages/",route_name="myimages")
def images(request, **params):
    if request.method == "POST":
        user = CustomUserInterface(**request.values)
        if user.is_valid:
            print("User is valid")
        else:
            print(user.is_valid)
            return HttpResponse(response_text=f"<h1>{user.is_valid}</h1>")

    print(params)
    print(request.headers)
    print("Cookies", request.cookies)
    # response = HttpResponse(status=status.PERMANENT_REDIRECT)
    # return response.redirect("/users/2/name/feruz-raxmonov/")
    return HttpResponse(status=status.OK, response_file="../frontend/index.html")