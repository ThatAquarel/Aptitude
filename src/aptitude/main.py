import multiprocessing
# noinspection PyPackageRequirements
from graphlib import TopologicalSorter

import spacy

from aptitude.literary_devices.characterization.characterization import Characterization
from aptitude.literary_devices.literary_device import LiteraryDevices
from aptitude.literary_devices.metaphor.metaphor import Metaphor
from aptitude.literary_devices.simile.simile import Simile
from aptitude.literary_devices.symbolism.symbolism import Symbolism
from aptitude.util.text import Text
from aptitude.util.types import Documents


class Aptitude:
    _documents: Documents
    _literary_devices: LiteraryDevices

    def __init__(self):
        nlp = spacy.load("en_core_web_trf")

        text = Text("./books/alice_in_wonderland.txt")
        sentences = text.get_sentences()

        for doc in nlp.pipe(sentences, n_process=multiprocessing.cpu_count()):
            self._documents.append(doc)

        self._literary_devices = self.instantiate_literary_devices()

    def instantiate_literary_devices(self) -> LiteraryDevices:
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
        for literary_device in classes.values():
            for dependency in literary_device.get_dependencies():
                dependencies[dependency.__name__].append(literary_device.__name__)

        names = {k: set(v) for k, v in dependencies.items()}
        sorted_names = list(TopologicalSorter(names).static_order())[::-1]

        return [classes[name](self._documents) for name in sorted_names]

    def parse_literary_devices(self) -> None:
        ...


if __name__ == "__main__":
    Aptitude()
