from abc import ABC, abstractmethod
from typing import TypeVar, Generic

from aptitude.pipeline.node import Node, NodeType

T = TypeVar("T")


class Parser(Node, ABC, Generic[T]):
    _output_data: T

    def process(self, data):
        self.parse(data)

    @abstractmethod
    def parse(self, data):
        raise NotImplementedError("parse() of LiteraryDevice is not implemented")

    @staticmethod
    @abstractmethod
    def get_dependencies() -> list[type]:
        raise NotImplementedError("get_dependencies() of LiteraryDevice is not implemented")

    @staticmethod
    def get_node_type() -> NodeType:
        return NodeType.PARSER

    def get_output_data(self) -> T:
        return self._output_data
