import re


class Text:
    _text: str

    def __init__(self, path: str):
        with open(path, "r") as file:
            self._text = file.read()

    def get_sentences(self):
        return re.split("[.?!]", self._text)
