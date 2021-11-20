from abc import ABC, abstractmethod
from enum import Enum

from aptitude.util.types import Documents, PipelineData


class NodeType(Enum):
    GENERIC = 0
    PARSER = 1


class Node(ABC):
    _docs: Documents

    def __init__(self, docs: Documents):
        self._docs = docs

    @abstractmethod
    def process(self, data: PipelineData) -> None:
        raise NotImplementedError("process() of Node is not implemented")

    @staticmethod
    @abstractmethod
    def get_dependencies() -> list[type]:
        raise NotImplementedError("get_dependencies() of Node is not implemented")

    @staticmethod
    def get_node_type() -> NodeType:
        return NodeType.GENERIC


Nodes = list[Node]
