import spacy
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from character_relation.config import MAX_TOKEN_LENGTH, SPACY_NLP_MODEL, SPACY_WORD_VEC_SIZE


class Softmax2D(layers.Layer):
    def __init__(self, output_shape_=(-1, 2), **kwargs):
        super().__init__(**kwargs)
        self.output_shape_ = output_shape_

    def call(self, inputs, **kwargs):
        len_input = tf.shape(inputs)[0]
        reshaped = tf.reshape(inputs, shape=(len_input, *self.output_shape_))
        return tf.nn.softmax(reshaped, axis=-1)


class CharacterRelationModel:
    def __init__(self):
        self._nlp = spacy.load(SPACY_NLP_MODEL)

    def preprocess(self, texts: list[str]) -> np.ndarray:
        docs = list(self._nlp.pipe(texts))
        doc_vectors = [
            [token.vector for token in doc if token.is_alpha][:MAX_TOKEN_LENGTH]
            for doc in docs
        ]

        inputs = np.zeros((len(docs), MAX_TOKEN_LENGTH, SPACY_WORD_VEC_SIZE))
        for i, vectors in enumerate(doc_vectors):
            inputs[i, np.arange(len(vectors)), :] = vectors

        return inputs

    @staticmethod
    def get_model():
        # Input shape  Layer       Output shape
        # =====================================
        # (*, 32, 300) Masking     (*, 32, 300)
        # (*, 32, 300) LSTM        (*, 300)
        # (*, 300)     Dense       (*, 150)
        # (*, 150)     Dense       (*, 10)
        # (*, 10)      Softmax dim (*, 5, 2)

        return keras.Sequential([
            layers.Input(shape=(MAX_TOKEN_LENGTH, SPACY_WORD_VEC_SIZE,)),
            layers.Masking(),
            layers.LSTM(SPACY_WORD_VEC_SIZE),
            layers.Dense(SPACY_WORD_VEC_SIZE / 2, activation='relu'),
            layers.Dense(10),
            Softmax2D()
        ])
