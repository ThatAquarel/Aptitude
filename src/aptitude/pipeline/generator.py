from abc import ABC, abstractmethod
from typing import TypeVar, Generic

from aptitude.pipeline.node import Node, NodeType

T = TypeVar("T")


class Generator(Node, ABC, Generic[T]):
    def process(self, data) -> T:
        return self.generate(data)

    @abstractmethod
    def generate(self, data) -> T:
        raise NotImplementedError("generate() of Generator is not implemented")

    @staticmethod
    def get_node_type() -> NodeType:
        return NodeType.GENERATOR
