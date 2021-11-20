from aptitude.literary_devices.metaphor.metaphor import Metaphor
from aptitude.literary_devices.simile.simile import Simile
from aptitude.pipeline.parser import Parser


class Characterization(Parser):
    @staticmethod
    def get_dependencies() -> list[type]:
        return [Metaphor, Simile]

    def parse(self, data):
        pass
