import datetime
from http import cookies

cookie = cookies.Morsel()


def set_cookie(
    key: str,
    value: str,
    coded_value: str,
    httponly: bool = False,
    path: str = "/",
    days_expire: int = 7
) -> cookies.Morsel:

    if days_expire is None:
        max_age = 365 * 24 * 60 * 60  # one year
    else:
        max_age = days_expire * 24 * 60 * 60

    expires = datetime.datetime.strftime(
        datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age),
        "%a, %d-%b-%Y %H:%M:%S GMT")

    cookie.set(key, value, coded_value)
    cookie["max-age"] = max_age
    cookie["httponly"] = httponly
    cookie["domain"] = "127.0.0.1"
    cookie["secure"] = True
    cookie["path"] = path

    return cookie


def delete_cookie(self, key, path="/", domain=None, samesite=None):
    # Browsers can ignore the Set-Cookie header if the cookie doesn't use
    # the secure flag and:
    # - the cookie name starts with "__Host-" or "__Secure-", or
    # - the samesite is "none".
    secure = key.startswith(("__Secure-", "__Host-")) or (
        samesite and samesite.lower() == "none"
    )
    set_cookie(
        key,
        max_age=0,
        path=path,
        domain=domain,
        secure=secure,
        expires="Thu, 01 Jan 1970 00:00:00 GMT",
        samesite=samesite,
    )
