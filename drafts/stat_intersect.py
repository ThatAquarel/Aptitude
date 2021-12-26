import numpy as np


def get_probabilistic_intersection(sets) -> dict[str, float]:
    texts = [string for string in sets.keys()]
    global_counts = np.array([count for count in sets.values()], dtype=np.float32)
    weighted_average_length = np.average(np.char.str_len(texts), weights=global_counts)

    all_chars = [char for string in texts for char in string]
    unique_chars = np.unique(all_chars)

    def get_combination_probabilities(combinations):
        combination_count = np.array([
            np.char.count(texts, combination)
            for combination in combinations
        ])
        return np.average(combination_count, weights=global_counts, axis=-1)

    x, y = np.meshgrid(unique_chars, unique_chars)
    char_combinations = np.char.add(x, y).reshape(-1)

    char_combinations_probabilities = get_combination_probabilities(char_combinations)
    variation = round(weighted_average_length)
    probable_indices = np.argpartition(char_combinations_probabilities, -variation)[-variation:]

    probable_char_combinations = char_combinations[probable_indices]
    probable_char_probabilities = char_combinations_probabilities[probable_indices]
    probable_separated_chars = [[char for char in string] for string in probable_char_combinations]

    if np.all(probable_char_probabilities == probable_char_probabilities[0]):
        raise Exception("No two character intersection")

    if weighted_average_length < 3:
        return {
            combination: probability
            for combination, probability in
            zip(probable_char_combinations, probable_char_probabilities)
        }

    intersect_combinations = []
    for i, x in enumerate(probable_char_combinations):
        for j, y in enumerate(probable_separated_chars):
            if i == j:
                continue
            if y[0] in x:
                intersect_combinations.append(f"{x}{y[1]}")
            elif y[1] in x:
                intersect_combinations.append(f"{y[0]}{x}")
    intersect_combinations = np.unique(intersect_combinations)
    intersect_combinations_probabilities = get_combination_probabilities(intersect_combinations)

    return {
        combination: probability
        for combination, probability in
        zip(intersect_combinations, intersect_combinations_probabilities)
    }


def get_probable_string(probabilistic_intersection: dict[str, float]) -> str:
    texts = [i for i in probabilistic_intersection.keys()]
    probabilities = [i for i in probabilistic_intersection.values()]
    index = np.argmax(probabilities)

    return texts[index]


def main():
    print(get_probable_string(get_probabilistic_intersection({
        "abcd": 30,
        "bcde": 15,
        "bcd": 2,
        "cd": 5
    })))  # bcd

    print(get_probable_string(get_probabilistic_intersection({
        "cd": 40,
        "abd": 40,
        "bd": 40
    })))  # bd

    print(get_probable_string(get_probabilistic_intersection({
        "d": 40,
        "abd": 40,
        "bd": 40
    })))  # bd

    print(get_probable_string(get_probabilistic_intersection({
        "cd": 40,
        "ab": 40,
        "bd": 40
    })))  # Exception: No two character intersection


if __name__ == '__main__':
    main()
