import pickle

import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

MAX_TOKEN_LENGTH = 32


# class VectorEmbedding(layers.Layer):
#     def __init__(self, units=64, vec_size=300, **kwargs):
#         super().__init__(**kwargs)
#         self.units = units
#         self.vec_size = vec_size
#
#     def call(self, inputs, **kwargs):
#         embedding_size = [inputs.shape[0], self.units, self.vec_size]
#         embedding = tf.zeros(embedding_size, tf.float32)
#
#         len_tokens = tf.clip_by_value(inputs.shape[0], clip_value_min=1, clip_value_max=self.units)
#         idx_range = tf.range(len_tokens)
#
#         embedding[:, idx_range, :] = inputs
#         return embedding

class Softmax2D(layers.Layer):
    def __init__(self, output_shape_=(-1, 2), **kwargs):
        super().__init__(**kwargs)
        self.output_shape_ = output_shape_

    def call(self, inputs, **kwargs):
        len_input = tf.shape(inputs)[0]
        reshaped = tf.reshape(inputs, shape=(len_input, *self.output_shape_))
        return tf.nn.softmax(reshaped, axis=-1)


model = keras.Sequential([
    # (*, n tokens, 300) Embedding (*, 64, 300)
    # (*, 64, 300) LSTM (*, 300)
    # (*, 300) Dense (*, 150)
    # (*, 150) Dense (*, 10)
    # (*, 10) Softmax dim (*, 5, 2)

    layers.Input(shape=(MAX_TOKEN_LENGTH, 300,)),
    layers.LSTM(300),
    layers.Dense(150, activation='relu'),
    layers.Dense(10),
    Softmax2D()
])

model.build()
model.summary()

model.compile(loss=keras.losses.BinaryCrossentropy(from_logits=True),
              optimizer=keras.optimizers.Adam(1e-4),
              metrics=['accuracy'])

with open("data/dataset", "rb") as file:
    dataset = pickle.load(file)
model.fit(x=dataset['x'], y=dataset['y'], batch_size=64, epochs=128, validation_split=0.2)

model.save("character_relation_model")
