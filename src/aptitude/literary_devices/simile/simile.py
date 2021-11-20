from aptitude.pipeline.parser import Parser


class Simile(Parser):
    @staticmethod
    def get_dependencies() -> list[type]:
        return []

    def parse(self, data):
        pass
