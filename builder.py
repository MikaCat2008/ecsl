from typing import Callable
from collections import deque

from engine.core import Entity, Component

from .tools import get_properties
from .factory import EntityFactory, ComponentFactory
from .tokenizer import Tokenizer
from .syntax_tree import Node, SyntaxTree


class Builder:
    handlers: dict[str, Callable]
    entities: EntityFactory
    components: ComponentFactory

    tokenizer: Tokenizer
    syntax_tree: SyntaxTree

    def __init__(self, entities: EntityFactory, components: ComponentFactory) -> None:
        self.handlers = {}
        self.entities = entities
        self.components = components

        self.tokenizer = Tokenizer()
        self.syntax_tree = SyntaxTree()

    def add_section_handler(self, name: str, handler: Callable) -> None:
        self.handlers[name] = handler

    def handle_section(self, name: str, entity: Entity, section: deque[Node]) -> None:
        if name == "childs":
            entity.childs = self.build_entities_from_nodes(section)
        elif name == "components":
            for component in self.build_components_from_nodes(section):
                entity.add_component(component)
        else:
            handler = self.handlers.get(name)

            if handler:
                handler(entity, section)

    def build_entity_from_node(self, node: Node) -> Entity:
        entity = self.entities.create(node.name)

        for name, section in node.sections.items():
            self.handle_section(name, entity, section)

        return entity

    def build_entities_from_nodes(self, nodes: deque[Node]) -> deque[Entity]:
        entities = deque()

        for node in nodes:
            entities.append(self.build_entity_from_node(node))
        
        return entities

    def build_component_from_node(self, node: Node) -> Component:
        return self.components.create(
            node.name, 
            **get_properties(
                node.sections.get(None, deque())
            )
        )

    def build_components_from_nodes(self, nodes: deque[Node]) -> deque[Component]:
        components = deque()

        for node in nodes:
            components.append(self.build_component_from_node(node))

        return components

    def build_entities_from_text(self, text: str) -> deque[Entity]:
        tokens = self.tokenizer.tokenize(text)
        nodes = self.syntax_tree.parse(tokens)[None]

        return self.build_entities_from_nodes(nodes)
