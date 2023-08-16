from http import HTTPStatus as status
from urllib.parse import parse_qsl
from socks.tcp import TCPServer
from typing import (
    Any,
    Callable,
    Dict,
    Tuple
)
from .type import Response

from .request import Request
from .response import HttpResponse, HttpResponseRedirect
from .router import router
from .routes import *


class HTTPServer(TCPServer):

    def get_view_func(
        self,
        path: str
    ) -> Tuple[Callable[[Request], Response],
               Dict[str, Any]]:
        if path[-1] != "/":
            path = path + "/"

        return router.get_route(path)

    def response(self, data: bytes) -> Response:
        request = self.dispatch(data=data)
        view_func, params = self.get_view_func(request.path)
        if view_func is None:
            return HttpResponse(status=status.OK, response_text="<h1>View func not found<h1/>")
        print("REQ:=", request, params)
        response = view_func(request, **params)
        return response

    def dispatch(self, data: bytes) -> Request:
        print("Dispatched....")
        data = data.decode("utf-8")
        headers_list = data.split("\r\n")
        request_method_text = headers_list.pop(0)

        if len(request_method_text) < 2:
            return

        headers, values = self.get_headers(headers_list)
        method, path = self.get_method_path(request_method_text)

        request = {
            "headers": headers,
            "method": method,
            "path": path,
            "values": values,
        }

        return Request(**request)

    def get_method_path(self, request_method_text: str) -> tuple[str]:
        method, path, http_version = request_method_text.split(" ")
        print(f"Method {method} received")

        return (method, path)

    def get_headers(
        self,
        headers_list: list[str]
    ) -> Tuple[
            Dict[str, Any],
            Dict[str, Any]]:
        headers = {}
        for header in headers_list:
            splitted_header = header.split(": ")
            length = len(splitted_header)
            if length == 2:
                headers[splitted_header[0]] = splitted_header[1]
            elif length == 1:
                headers[splitted_header[0]] = None

        values = dict(parse_qsl(headers_list[-1]))

        return (headers, values)

    def handle_request(self, data: bytes) -> bytes:
        response = self.response(data)
        response_line = bytes(
            f"HTTP/1.1 {response.status.value} {response.status.phrase}\n{response.headers}\r\n".encode("utf-8"))

        print(response_line)
        blank_line = b"\r\n"

        return b"".join([
            response_line,
            blank_line,
            response.response_body])
