from typing import Type

from engine.core import Entity, Component


class EntityFactory:
    entities: dict[str, Type[Entity]]

    def __init__(self) -> None:
        self.entities = {}

    def create(self, name: str) -> Entity:
        return self.entities[name]()
    
    def extend(self, entities: dict[str, Type[Entity]]) -> None:
        self.entities |= entities


class ComponentFactory:
    components: dict[str, Type[Component]]

    def __init__(self) -> None:
        self.components = {}

    def create(self, name: str, **properties: object) -> Component:
        return self.components[name](**properties)

    def extend(self, components: dict[str, Type[Component]]) -> None:
        self.components |= components
