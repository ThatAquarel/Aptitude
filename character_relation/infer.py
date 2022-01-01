import spacy
import numpy as np

from tensorflow import keras

nlp = spacy.load("en_core_web_md")
model = keras.models.load_model("character_relation_model")


def preprocess(text: str):
    doc = nlp(text)
    vectors = [token.vector for token in doc]
    x = np.zeros((1, 32, 300))
    x[:, np.arange(len(vectors)), :] = vectors

    return x


model.predict(preprocess("My boss at work is extremely toxic, he insults everyone."))
model.predict(preprocess("He's my accomplice"))
model.predict(preprocess("He's my rival in a swimming competition"))
