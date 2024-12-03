from __future__ import annotations

from enum import Enum
from collections import deque

from .tokenizer import Token, TokenType

TAB = "  "


class StateType(Enum):
    NONE = 0
    GET_NODE_NAME = 1
    GET_ATTRIBUTE = 2


class Node:
    name: str
    sections: dict[str, deque[Node]]
    attributes: dict[str, object]

    def __init__(self, name: str) -> None:
        self.name = name
        self.sections = {}
        self.attributes = {}

    def to_string(self, deep: int = 0) -> str:
        attributes = ' '.join(
            f'{attribute}={"" if isinstance(value, str) else "v"}"{value}"'
            for attribute, value in self.attributes.items()
        )

        if attributes:
            attributes = " " + attributes

        sections_str = ""

        for section, childs in self.sections.items():
            section_str = "\n" + TAB * deep + f"{section}: \n"
            
            for child in childs:
                section_str += TAB * (deep + 1) + child.to_string(deep + 1)
            
            sections_str += section_str

        if sections_str:
            sections_str += f"\n{TAB * deep}"

            return f"<{self.name}{attributes}>{sections_str}</{self.name}>"
        return f"<{self.name}{attributes} />"

    def __repr__(self) -> str:
        return self.to_string()


class SyntaxTree:
    def _parse(self, tokens: deque[Token], i: int = 0) -> tuple[int, dict[str, deque[Node]]]:
        state = StateType.NONE
        sections = {}
        current_node = None
        current_section_name = None
        current_section_nodes = deque()

        while i < len(tokens):
            token = tokens[i]

            if token.type == TokenType.LEFT_BRACKET:
                state = StateType.GET_NODE_NAME

            elif token.type == TokenType.NAME:
                if state == StateType.GET_NODE_NAME:
                    state = StateType.GET_ATTRIBUTE
                    current_node = Node(token.value)
                elif state == StateType.GET_ATTRIBUTE:
                    attribute_name = token.value

                    token_p1 = tokens[i + 1]
                    token_p2 = tokens[i + 2]

                    if token_p1.type == TokenType.EQUAL:
                        attribute_value = token_p2.value

                        i += 2
                    else:
                        attribute_value = None

                    if token_p2.type == TokenType.VALUE_STRING:
                        attribute_value = eval(attribute_value)

                    current_node.attributes[attribute_name] = attribute_value
                else:
                    if current_section_nodes:
                        sections[current_section_name] = current_section_nodes

                    current_section_name = token.value
                    current_section_nodes = deque()

                    state = StateType.NONE

            elif token.type == TokenType.RIGHT_BRACKET:
                if tokens[i - 1].type == TokenType.SLASH:
                    current_section_nodes.append(current_node)
                    current_node = None
                elif tokens[i - 2].type != TokenType.SLASH:
                    i, current_node.sections = self._parse(tokens, i + 1)

                    current_section_nodes.append(current_node)
        
                    current_node = None
    
                state = StateType.NONE

            elif token.type == TokenType.SLASH:
                if current_section_nodes:
                    sections[current_section_name] = current_section_nodes
                
                if current_node is None:
                    return i + 2, sections

            i += 1

        if current_section_nodes:
            sections[current_section_name] = current_section_nodes

        return i, sections

    def parse(self, tokens: deque[Token]) -> deque[Node]:
        return self._parse(tokens)[1]
