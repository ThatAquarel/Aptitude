import pickle
import numpy as np

from character_relation.config import MAX_TOKEN_LENGTH
from character_relation.data.words import criteria_words as criteria_words_
from character_relation.data.words import filler_words as filler_words_
from character_relation.model import CharacterRelationModel

SENTENCES_PER_TYPE = 2
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

    data = {
        'x': x,
        'y': y
    }
    with open("dataset", "wb") as file:
        pickle.dump(data, file)


if __name__ == '__main__':
    main()