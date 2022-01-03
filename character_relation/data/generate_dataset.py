import importlib
import pickle

import numpy as np
import tensorflow as tf

from character_relation.config import MAX_TOKEN_LENGTH, LANGUAGE
from character_relation.model import CharacterRelationModel

words = importlib.import_module(f"character_relation.data.words_{LANGUAGE}")
criteria_words_ = words.criteria_words
filler_words_ = words.filler_words

SENTENCES_PER_TYPE = 8
SHUFFLE_QTY = 3


def main():
    permutations = np.meshgrid(*[np.arange(3) for _ in range(5)])
    permutations = np.array(permutations).reshape((5, -1)).T
    permutations = np.repeat(permutations, SENTENCES_PER_TYPE, axis=0)
    permutations = permutations[:, ::-1]

    filler_words = np.array(filler_words_)
    criteria_words = np.array(criteria_words_, dtype=list).reshape((5, -1))
    sentences = []
    y = np.zeros((permutations.shape[0], 5, 2), dtype=np.float32)
    for i, permutation in enumerate(permutations):
        mask = permutation.astype(bool)
        random_filler_idx = np.random.randint(0, len(filler_words), MAX_TOKEN_LENGTH)
        random_filler_idx = random_filler_idx[np.add.reduce(mask):]
        words_list = filler_words[random_filler_idx].tolist()

        criteria_words_list = criteria_words[mask]
        permutation = permutation[mask]
        for perm, criteria in zip(permutation, criteria_words_list):
            criterion = criteria[perm - 1]
            words_list.append(criterion[np.random.randint(0, len(criterion))])

        for _ in range(SHUFFLE_QTY):
            np.random.shuffle(words_list)

        sentences.append(' '.join(words_list))
        y[i, mask, permutation - 1] = 1

    character_relation_model = CharacterRelationModel()
    x = character_relation_model.preprocess(sentences)
    y = tf.nn.softmax(y, axis=-1).numpy()

    data = {
        'x': x,
        'y': y
    }
    with open(f"dataset_{LANGUAGE}", "wb") as file:
        pickle.dump(data, file)


if __name__ == '__main__':
    main()
