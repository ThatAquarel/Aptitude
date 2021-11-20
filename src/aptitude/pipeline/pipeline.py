from abc import ABC, abstractmethod
from graphlib import TopologicalSorter

from aptitude.pipeline.node import Nodes, Node, NodeType, NodeClasses
from aptitude.util.types import PipelineData


class Pipeline(ABC):
    _nodes: Nodes
    _pipeline_data: PipelineData

    @abstractmethod
    def get_node_classes(self) -> NodeClasses:
        raise NotImplementedError("get_nodes() of Pipeline is not implemented")

    def instantiate_nodes(self) -> None:
        generators = [
            class_ for class_ in self.get_node_classes()
            if class_.get_node_type() == NodeType.GENERATOR
        ]
        parsers = [
            class_ for class_ in self.get_node_classes()
            if class_.get_node_type() != NodeType.GENERATOR
        ]

        self._nodes = []
        self._nodes.extend(self._resolve_dependencies(generators))
        self._nodes.extend(self._resolve_dependencies(parsers))

    @staticmethod
    def _resolve_dependencies(nodes: NodeClasses) -> list[Node]:
        classes = {class_.__name__: class_ for class_ in nodes}
        dependencies = {class_.__name__: [] for class_ in classes.values()}

        for node in classes.values():
            for dependency in node.get_dependencies():
                dependencies[dependency.__name__].append(node.__name__)

        names = {k: set(v) for k, v in dependencies.items()}
        sorted_names = list(TopologicalSorter(names).static_order())[::-1]

        return [classes[name]() for name in sorted_names]

    def process_nodes(self):
        _pipeline_data = {}

        for node in self._nodes:
            _pipeline_data[node.__class__] = node.process(_pipeline_data)
