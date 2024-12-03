from typing import Optional
from collections import deque

from .syntax_tree import Node


def get_properties(section: dict[Optional[str], deque[Node]]) -> dict[str, object]:
    return {
        child.attributes["name"]: child.attributes["value"]
        for child in section
        if child.name == "property"
    }
