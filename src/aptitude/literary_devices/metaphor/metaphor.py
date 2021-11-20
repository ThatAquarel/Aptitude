from aptitude.literary_devices.literary_device import LiteraryDevice


class Metaphor(LiteraryDevice):
    @staticmethod
    def get_dependencies() -> list[type]:
        return []

    def parse(self):
        pass
