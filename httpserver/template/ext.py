from jinja2.ext import Extension

from typing import (
    Union,
    List,
    TYPE_CHECKING
)

from jinja2.nodes import ContextReference, Node, Output
from jinja2 import nodes

if TYPE_CHECKING:
    from jinja2.parser import Parser
    from jinja2.nodes import Nodes


class StaticExtension(Extension):
    tags = {"static"}
    ext_attr = 42
    context_reference_node_cls = ContextReference

    def parse(self, parser: "Parser") -> Union[Node, List[Node]]:
        return nodes.Output(
            [
                self.call_method(
                    "_dump",
                    [
                        nodes.EnvironmentAttribute("sandboxed"),
                        self.attr("ext_attr"),
                        nodes.ImportedName(__name__ + ".importable_object"),
                        self.context_reference_node_cls(),
                    ],
                )
            ]
        ).set_lineno(next(parser.stream).lineno)

    def _dump(self, sandboxed, ext_attr, imported_object, context):
        print("ext attr", ext_attr)
        return (
            f"{sandboxed}|{ext_attr}|{imported_object}|{context.blocks}"
            f"|{context.get('static_var')}"
        )
