from aptitude.literary_devices.literary_device import LiteraryDevice
from aptitude.literary_devices.metaphor.metaphor import Metaphor
from aptitude.literary_devices.simile.simile import Simile


class Characterization(LiteraryDevice):
    @staticmethod
    def get_dependencies() -> list[type]:
        return [Metaphor, Simile]

    def parse(self):
        pass
