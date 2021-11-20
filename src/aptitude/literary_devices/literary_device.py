from abc import ABC, abstractmethod
from typing import TypeVar, Generic

from aptitude.util.types import Documents

T = TypeVar("T")


class LiteraryDevice(ABC, Generic[T]):
    _docs: Documents
    _output_data: T

    def __init__(self, docs: Documents):
        self._docs = docs

    @abstractmethod
    def parse(self):
        raise NotImplementedError("parse() of LiteraryDevice is not implemented")

    @staticmethod
    @abstractmethod
    def get_dependencies() -> list[type]:
        raise NotImplementedError("get_dependencies() of LiteraryDevice is not implemented")

    def get_output_data(self) -> T:
        return self._output_data


LiteraryDevices = list[LiteraryDevice]
