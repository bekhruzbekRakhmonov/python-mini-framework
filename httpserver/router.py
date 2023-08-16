import typing
from typing import (
    Any,
    Callable,
    Dict,
    Tuple,
    Union
)

from urllib import parse
import re

from .exceptions import RouterException

if typing.TYPE_CHECKING:
    from .request import Request
    from . import type as types


class Router:
    routes: dict = {}

    def route(
        self,
        path: str,
        func: Callable[["Request"], "types.Response"],
        name: str
    ) -> None:

        self.routes[path] = func
        self.routes[name] = path

    def get_route(
        self,
        req_path: str
    ) -> Callable[["Request"], "types.Response"]:

        keys = self.routes.keys()
        valid_key, params = self.get_valid_key(keys, req_path)

        if valid_key == None:
            return None,None

        """
            req_path -> /users/2/
            our path-> /users/:id/
        """
        view_func = self.routes[valid_key]
        return view_func, params

    def get_valid_key(
        self,
        keys: Dict[str, Callable[["Request"], "BaseResponse"]],
        req_path: str
    ) -> Tuple[Union[str, None], Dict]:

        params = {}
        for key in keys:
            params_list = re.findall(r":([^/]+)", key)

            if key == req_path and len(params_list) == 0:
                return key, params

            splitted_key = key.split("/")
            splitted_req_path = req_path.split("/")

            # I will use filter() Inshallah
            if len(splitted_key) == len(splitted_req_path):
                idxs = [splitted_key.index(f":{p}") for p in params_list]
                for idx in idxs:
                    param_name, param_value = splitted_key[idx], splitted_req_path[idx]
                    params[param_name.lstrip(":")] = parse.unquote_plus(
                        param_value)  # %20 -> +
                    splitted_key[idx], splitted_req_path[idx] = "", ""
                if splitted_key == splitted_req_path:
                    return key, params
                else:
                    params = {}
        return None, params

    def get_router_by_name(self, name: str) -> Tuple[str, bool]:
        route_path = self.routes.get(name)

        if route_path is None:
            raise RouterException(f"{name} is not a valid view name.")

        params = {}
        params_list = re.findall(r":([^/]+)", route_path)
        if len(params_list) == 0:
            return route_path, False

        splitted_route_path = route_path.split("/")

        idxs = [splitted_route_path.index(f":{p}") for p in params_list]
        for idx in idxs:
            splitted_route_path[idx] = "%s"

        route_path = "/".join(s for s in splitted_route_path)
        print(route_path)
        return route_path, True


router = Router()

def route(
    route_path: str,
    route_name: str
    ) -> Callable[["Request"], "types.Response"]:
    def decorator(func: Callable[["Request"], "types.Response"]):
        router.route(func=func,path=route_path,name=route_name)
        # def wrapper(request: "Request", **params: Dict[str,Any]):
        #     router.route(func=func,path=route_path,name=route_name)
        #     return func

        # return wrapper

    return decorator