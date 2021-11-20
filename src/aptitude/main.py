from aptitude.nodes.literary_devices.characterization.characterization import Characterization
from aptitude.nodes.literary_devices.metaphor.metaphor import Metaphor
from aptitude.nodes.literary_devices.simile.simile import Simile
from aptitude.nodes.literary_devices.symbolism.symbolism import Symbolism
from aptitude.nodes.nlp import Nlp
from aptitude.nodes.text import Text
from aptitude.pipeline.pipeline import Pipeline


class Aptitude(Pipeline):
    def get_node_classes(self) -> list[type]:
        return [
            Text,
            Nlp,
            Characterization,
            Metaphor,
            Simile,
            Symbolism
        ]

    def __init__(self):
        self.instantiate_nodes()
        self.process_nodes()


if __name__ == "__main__":
    Aptitude()
