from http import HTTPStatus

from typing import (
    Any,
    Dict,
    Optional
)

from . import cookie

HOST = "http://127.0.0.1:8000"


class BaseResponse:
    """BaseResponse class"""

    def __init__(
        self,
        status: HTTPStatus = HTTPStatus.OK,
        response_text: Optional[str] = None,
        response_file: Optional[str] = None,
        headers: Optional[Dict[str, Any]] = None
    ):
        self.header = ""
        self.status = status
        self.response_body = b""
        self.response_text = response_text
        self.response_file = response_file

        if headers is not None:
            self.set_headers(headers)

    @property
    def headers(self):
        return self.header

    def set_headers(self, headers: Optional[Dict[str, Any]] = None, header: Optional[str] = None):
        if headers != None and header == None:
            header = ""

            for key in headers:
                header += key + ": " + headers[key] + "\n"

            self.header += header

        elif headers == None and header != None:
            self.header += header

        else:
            raise Exception("Header not found.")

    def __str__(self):
        return self.__class__.__name__


class HttpResponse(BaseResponse):
    """Simple HttpResponse class"""

    def __init__(self, **kwargs):
        super(HttpResponse, self).__init__(**kwargs)
        self.response_body = self.get_response(
            self.response_text, self.response_file)

    def get_response(
        self,
        response_text: str,
        response_file: str
    ) -> bytes:
        if response_file is not None:
            response_body = self.get_encoded_response_file_body(
                response_file)
        elif response_text is not None:
            encoded = response_text.encode("utf-8")
            response_body = bytes(encoded)
        elif not any([response_text, response_file]):
            response_body = b""
        return response_body

    def get_encoded_response_file_body(
        self,
        response_file: str
    ) -> bytes:
        try:
            file = open(response_file, "rb")
            response_body = file.read()
        except FileNotFoundError:
            response_body = b"Response file not found"

        return response_body

    def set_cookie(
            self,
            key: str,
            value: str,
            coded_value: str,
            **kwargs) -> str:
        c = cookie.set_cookie(key=key, value=value,
                              coded_value=coded_value, **kwargs)
        header = c.output()
        return self.set_headers(header=header)

    def redirect(self, path: str) -> BaseResponse:
        headers = {"Location": HOST + path}
        self.set_headers(headers=headers)
        return self

    def __call__(self):
        return (self.status, self.response_body, self.headers)


class HttpResponseRedirect(BaseResponse):
    def __init__(self, redirect_to, args, **kwargs):
        super(Redirect, self).__init__(**kwargs)
        self.redirect_to = redirect_to
        self.args = args
        self.status = status.PERMANENT_REDIRECT

        self.redirect()

    def redirect(self):
        route_path, args_required = router.get_router_by_name(
            self.redirect_to)

        if args_required:
            route_path = route_path % self.args

        headers = {}
        headers["Location"] = HOST + route_path
        self.set_headers(headers=headers)

# res = HttpResponse(status=200, response_file="index.html")
# print(res())
