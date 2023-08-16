from typing import Union

from .response import HttpResponse, HttpResponseRedirect

Response = Union[HttpResponse, HttpResponseRedirect]
