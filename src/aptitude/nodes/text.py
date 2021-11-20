from aptitude.config import TEXT_PATH
from aptitude.pipeline.generator import Generator, T
import re


class Text(Generator):
    def generate(self, data) -> T:
        with open(TEXT_PATH, 'r') as file:
            text = file.read()

        return re.split("[.?!]", text)

    @staticmethod
    def get_dependencies() -> list[type]:
        return []
