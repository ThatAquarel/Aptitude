import pickle
import itertools
import numpy as np


def get_criteria_word_vectors(filename):
    with open(filename, "rb") as file:
        return pickle.load(file)


def main():
    criteria_vec = get_criteria_word_vectors("criteria_vectors")

    combination_mask = np.array(list(itertools.product([False, True], repeat=5)), dtype=int)
    vec_combinations = criteria_vec[np.arange(criteria_vec.shape[0]), combination_mask]

    print()


if __name__ == '__main__':
    main()
