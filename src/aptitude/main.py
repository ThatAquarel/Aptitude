import multiprocessing
# noinspection PyPackageRequirements
from graphlib import TopologicalSorter

import spacy

from aptitude.literary_devices.characterization.characterization import Characterization
from aptitude.literary_devices.metaphor.metaphor import Metaphor
from aptitude.literary_devices.simile.simile import Simile
from aptitude.literary_devices.symbolism.symbolism import Symbolism
from aptitude.pipeline.node import Nodes
from aptitude.util.text import Text
from aptitude.util.types import Documents


class Aptitude:
    _documents: Documents
    _nodes: Nodes

    def __init__(self):
        nlp = spacy.load("en_core_web_trf")

        text = Text("./books/alice_in_wonderland.txt")
        sentences = text.get_sentences()

        for doc in nlp.pipe(sentences, n_process=multiprocessing.cpu_count()):
            self._documents.append(doc)

        self._nodes = self.instantiate_nodes()

    def instantiate_nodes(self) -> Nodes:
        classes = {
            class_.__name__: class_
            for class_ in [
                Characterization,
                Metaphor,
                Simile,
                Symbolism
            ]
        }

        dependencies = {class_.__name__: [] for class_ in classes.values()}
        for node in classes.values():
            for dependency in node.get_dependencies():
                dependencies[dependency.__name__].append(node.__name__)

        names = {k: set(v) for k, v in dependencies.items()}
        sorted_names = list(TopologicalSorter(names).static_order())[::-1]

        return [classes[name](self._documents) for name in sorted_names]

    def parse_literary_devices(self) -> None:
        ...


if __name__ == "__main__":
    Aptitude()
