from typing import Callable
import re
from .router import router
from . import views

router.route("/users/:id/name/:name/", views.index, name="index")
router.route("/images/:type/", views.images, name="images")
router.route("/view/",views.View(), name="class-view")