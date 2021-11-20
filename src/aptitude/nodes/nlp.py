import multiprocessing

import spacy

from aptitude.config import NLP_MODEL
from aptitude.nodes.text import Text
from aptitude.pipeline.generator import Generator, T
from aptitude.util.serialization import serialized_cache


class Nlp(Generator):
    @serialized_cache
    def generate(self, data) -> T:
        documents = []
        sentences = data[Text]

        nlp = spacy.load(NLP_MODEL)

        for doc in nlp.pipe(sentences, n_process=multiprocessing.cpu_count()):
            documents.append(doc)

        return documents

    @staticmethod
    def get_dependencies() -> list[type]:
        return [Text]
