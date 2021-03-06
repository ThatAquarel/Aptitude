from abc import ABC, abstractmethod
from typing import TypeVar, Generic

from aptitude.pipeline.node import Node, NodeType

T = TypeVar("T")


class Parser(Node, ABC, Generic[T]):
    def process(self, data) -> T:
        return self.parse(data)

    @abstractmethod
    def parse(self, data) -> T:
        raise NotImplementedError("parse() of Parser is not implemented")

    @staticmethod
    def get_node_type() -> NodeType:
        return NodeType.PARSER
