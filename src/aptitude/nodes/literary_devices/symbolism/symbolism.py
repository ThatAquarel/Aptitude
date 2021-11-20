from aptitude.nodes.literary_devices.characterization.characterization import Characterization
from aptitude.nodes.literary_devices.metaphor.metaphor import Metaphor
from aptitude.nodes.literary_devices.simile.simile import Simile
from aptitude.pipeline.parser import Parser


class Symbolism(Parser):
    @staticmethod
    def get_dependencies() -> list[type]:
        return [Characterization, Metaphor, Simile]

    def parse(self, data):
        pass
