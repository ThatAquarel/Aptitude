import spacy
import numpy as np

# nlp = spacy.load("en_core_web_lg")
nlp = spacy.load("zh_core_web_lg")

# docs = [
#     nlp("Alice walks"),
#     nlp("thought Alice"),
#     nlp("Alice went after"),
#     nlp("said Alice"),
#     nlp("Alice was beginning to get very tired"),
#     nlp("Alice"),
#     nlp("The White Rabbit"),
#     nlp("Wonderland"),
#     nlp("Dinah the cat"),
#     nlp("The Mouse")
# ]

docs = [
    nlp("夏天依"),
    nlp("夏天来了"),
    nlp("夏天依游泳"),
    nlp("夏天依说"),
    nlp("夏天依赖地球公转"),
]

WORD_VEC_LENGTH = 300

# VEC SIMILARITY
# length = len(docs)
# cols = np.repeat(np.array(docs, dtype=object), length).reshape((length, length))
# rows = cols.T
#
# similarity_map = np.zeros((length, length), dtype=np.float32)
# for x in range(length):
#     for y in range(length):
#         similarity_map[x, y] = cols[x, y].similarity(rows[x, y])
# distribution = np.add.reduce(similarity_map)
# print(docs[np.argmin(distribution)])

# DIFFERENCE SIMILARITY
entity_vectors = [[token.vector for token in doc] for doc in docs]  # (5, n, 300)
vectors = np.array([np.add.reduce(vec) for vec in entity_vectors])  # (5, 300)
length = vectors.shape[0]  # 5

cols = np.tile(vectors, (1, length)).reshape((-1, length, WORD_VEC_LENGTH))  # (5, 5, 300)
rows = np.rot90(cols)  # (5, 5, 300)

diff_map = np.add.reduce(cols - rows, axis=2)  # (5,300)
distribution = np.abs(np.add.reduce(diff_map))  # (5)

print(docs[np.argmin(distribution)])
