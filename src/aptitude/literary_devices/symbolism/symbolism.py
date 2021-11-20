from aptitude.literary_devices.characterization.characterization import Characterization
from aptitude.literary_devices.literary_device import LiteraryDevice
from aptitude.literary_devices.metaphor.metaphor import Metaphor
from aptitude.literary_devices.simile.simile import Simile


class Symbolism(LiteraryDevice):
    @staticmethod
    def get_dependencies() -> list[type]:
        return [Characterization, Metaphor, Simile]

    def parse(self):
        pass
