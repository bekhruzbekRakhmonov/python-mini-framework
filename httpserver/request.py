from typing import (
    Any,
    Dict
)

class Request:
    def __init__(
        self, headers: Dict[str,Any], 
        method: str, 
        path:str, 
        values: Dict[str,Any]
        ):
    
        self.headers = headers
        self.method = method
        self.path = path
        self.values = values

    # def __getattr__(self,name):
    #     return self.request.get(name,None)

    @property
    def cookies(self):
        cookie = self.headers.get("Cookie")
        if cookie is None:
            return
        cookies = {}
        cookies_list = cookie.split(";")

        for c in cookies_list:
            key, value = c.split("=")
            cookies[key] = value

        return cookies
