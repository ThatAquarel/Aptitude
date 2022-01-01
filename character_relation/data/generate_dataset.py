import spacy
import pickle
import numpy as np

DATA_QTY = 100

nlp = spacy.load("en_core_web_lg")

with open("words.txt", "r") as file:
    text = file.read()
doc = nlp(text)
filler_vectors = np.array([token.vector for token in doc])
random_indices = np.random.randint(0, len(filler_vectors), (DATA_QTY, 31))
random_filler_vectors = filler_vectors[random_indices]

with open("criteria_data", "rb") as file:
    data = pickle.load(file)
one_hot_softmax = data["one_hot_softmax"]
vectors = data["vectors"]
random_indices = np.random.randint(0, len(vectors), (DATA_QTY, 1))
random_vectors = vectors[random_indices]
random_one_hot_softmax = one_hot_softmax[random_indices.reshape(-1)]

dataset_vectors = np.concatenate((random_filler_vectors, random_vectors), axis=1)
[np.random.shuffle(x) for x in dataset_vectors]

dataset = {
    "x": dataset_vectors,
    "y": random_one_hot_softmax
}
with open("dataset", "wb") as file:
    pickle.dump(dataset, file)
