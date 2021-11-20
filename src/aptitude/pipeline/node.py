from abc import ABC, abstractmethod
from enum import Enum

from aptitude.util.types import Documents, PipelineData


class NodeType(Enum):
    GENERIC = 0
    GENERATOR = 1
    PARSER = 2


class Node(ABC):
    _docs: Documents

    @abstractmethod
    def process(self, data: PipelineData) -> object:
        raise NotImplementedError("process() of Node is not implemented")

    @staticmethod
    @abstractmethod
    def get_dependencies() -> list[type]:
        raise NotImplementedError("get_dependencies() of Node is not implemented")

    @staticmethod
    def get_node_type() -> NodeType:
        return NodeType.GENERIC


Nodes = list[Node]
NodeClasses = list[Node.__class__]
