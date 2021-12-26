import numpy as np

SET_VARIATION = 3

# sets = {
#     "abcd": 30,
#     "bcde": 15,
#     "bcd": 2,
#     "cd": 5
# }
# bcd

# sets = {
#     "cd": 40,
#     "ab": 40,
#     "bd": 40
# }
# Exception: No two character intersection

sets = {
    "cd": 40,
    "abd": 40,
    "bd": 40
}

texts = [string for string in sets.keys()]
global_counts = [count for count in sets.values()]

all_chars = [char for string in texts for char in string]
unique_chars = np.unique(all_chars)


def get_combination_probabilities(combinations):
    combination_count = np.array([
        np.char.count(texts, combination)
        for combination in combinations
    ])
    return np.average(combination_count, weights=global_counts, axis=-1)


# stage 1
x, y = np.meshgrid(unique_chars, unique_chars)
char_combinations = np.char.add(x, y).reshape(-1)

char_combinations_probabilities = get_combination_probabilities(char_combinations)
probable_indices = np.argpartition(char_combinations_probabilities, -SET_VARIATION)[-SET_VARIATION:]

# char_combinations_probabilities = char_combinations_probabilities[probable_indices]
# if np.all(char_combinations_probabilities == char_combinations_probabilities[0]):
#     raise Exception("No two character intersection")

probable_char_combinations = char_combinations[probable_indices]
probable_separated_chars = [[char for char in string] for string in probable_char_combinations]

# stage 2
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
print(intersect_combinations[np.argmax(intersect_combinations_probabilities)])
