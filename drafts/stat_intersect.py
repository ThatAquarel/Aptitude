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

    permute_x, permute_y = np.meshgrid(unique_chars, unique_chars)
    char_combinations = np.char.add(permute_x, permute_y).reshape(-1)

    char_combinations_probabilities = get_combination_probabilities(char_combinations)
    variation = round(weighted_average_length)
    probable_indices = np.argpartition(char_combinations_probabilities, -variation)[-variation:]

    intersect_combinations = char_combinations[probable_indices]
    intersect_combinations_probabilities = char_combinations_probabilities[probable_indices]

    if np.all(intersect_combinations_probabilities == intersect_combinations_probabilities[0]):
        raise Exception("No two character intersection")

    if weighted_average_length < 3:
        return {
            combination: probability
            for combination, probability in
            zip(intersect_combinations, intersect_combinations_probabilities)
        }

    def get_intersections(combinations):
        intersections = []
        for i, x in enumerate(combinations):
            for j, y in enumerate(combinations):
                if i == j:
                    continue
                y = [char for char in y]

                if y[0] == x[-1]:
                    intersections.append(f"{x}{''.join(y[1:])}")
                elif y[-1] == x[0]:
                    intersections.append(f"{''.join(y[:-1])}{x}")

                if ''.join(y[:-1]) == x[1:]:
                    intersections.append(f"{x}{y[-1]}")
                elif ''.join(y[1:]) == x[:-1]:
                    intersections.append(f"{y[0]}{x}")

        return np.unique(intersections)

    intersect_combinations = get_intersections(intersect_combinations)
    intersect_combinations_probabilities = get_combination_probabilities(intersect_combinations)

    if np.unique(intersect_combinations_probabilities).shape[0] == intersect_combinations_probabilities.shape[0]:
        return {
            combination: probability
            for combination, probability in
            zip(intersect_combinations, intersect_combinations_probabilities)
        }

    # get indices of two duplicated probabilities
    idx_sort = np.argsort(intersect_combinations_probabilities)
    sorted_records_array = intersect_combinations_probabilities[idx_sort]
    values, idx_start, count = np.unique(sorted_records_array, return_counts=True, return_index=True)
    values = values[count > 1]
    res = np.split(idx_sort, idx_start[1:])
    res = list(filter(lambda x: x.size > 1, res))[0]

    intersect_combinations = intersect_combinations[res]
    intersect_combinations = get_intersections(intersect_combinations)

    if len(intersect_combinations) != 1:
        raise Exception("Illegal state")
    return {intersect_combinations[0]: values[0]}


def get_probable_string(probabilistic_intersection: dict[str, float]) -> str:
    texts = [i for i in probabilistic_intersection.keys()]
    probabilities = [i for i in probabilistic_intersection.values()]
    index = np.argmax(probabilities)

    return texts[index]


def main():
    print(get_probable_string(get_probabilistic_intersection({
        "abcde": 30,
        "febcde": 15,
        "bcdefgh": 2,
        "cd": 5
    })))  # bcde

    print(get_probable_string(get_probabilistic_intersection({
        "abcd": 30,
        "bcde": 15,
        "bcd": 2,
        "cd": 5
    })))  # bcd

    print(get_probable_string(get_probabilistic_intersection({
        "abcde": 30,
        "febcde": 15,
        "bcdefgh": 2,
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
