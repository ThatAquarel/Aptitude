import numpy as np


# def get_probabilistic_intersection(sets) -> dict[str, float]:
#     texts = [string for string in sets.keys()]
#     global_counts = np.array([count for count in sets.values()], dtype=np.float32)
#     weighted_average_length = np.average(np.char.str_len(texts), weights=global_counts)
#
#     all_chars = [char for string in texts for char in string]
#     unique_chars = np.unique(all_chars)
#
#     def get_combination_probabilities(combinations):
#         combination_count = np.array([
#             np.char.count(texts, combination)
#             for combination in combinations
#         ])
#         return np.average(combination_count, weights=global_counts, axis=-1)
#
#     permute_x, permute_y = np.meshgrid(unique_chars, unique_chars)
#     char_combinations = np.char.add(permute_x, permute_y).reshape(-1)
#
#     char_combinations_probabilities = get_combination_probabilities(char_combinations)
#     variation = round(weighted_average_length)
#     probable_indices = np.argpartition(char_combinations_probabilities, -variation)[-variation:]
#
#     intersect_combinations = char_combinations[probable_indices]
#     intersect_combinations_probabilities = char_combinations_probabilities[probable_indices]
#
#     if np.all(intersect_combinations_probabilities == intersect_combinations_probabilities[0]):
#         raise Exception("No two character intersection")
#
#     if weighted_average_length <= 3:
#         return {
#             combination: probability
#             for combination, probability in
#             zip(intersect_combinations, intersect_combinations_probabilities)
#         }
#
#     def get_intersections(combinations):
#         intersections = []
#         for i, x in enumerate(combinations):
#             for j, y in enumerate(combinations):
#                 if i == j:
#                     continue
#                 y = [char for char in y]
#
#                 if y[0] == x[-1]:
#                     intersections.append(f"{x}{''.join(y[1:])}")
#                 elif y[-1] == x[0]:
#                     intersections.append(f"{''.join(y[:-1])}{x}")
#
#                 if ''.join(y[:-1]) == x[1:]:
#                     intersections.append(f"{x}{y[-1]}")
#                 elif ''.join(y[1:]) == x[:-1]:
#                     intersections.append(f"{y[0]}{x}")
#
#         return np.unique(intersections)
#
#     intersect_combinations = get_intersections(intersect_combinations)
#     intersect_combinations_probabilities = get_combination_probabilities(intersect_combinations)
#
#     if np.unique(intersect_combinations_probabilities).shape[0] == intersect_combinations_probabilities.shape[0]:
#         return {
#             combination: probability
#             for combination, probability in
#             zip(intersect_combinations, intersect_combinations_probabilities)
#         }
#
#     # get indices of two duplicated probabilities
#     idx_sort = np.argsort(intersect_combinations_probabilities)
#     sorted_records_array = intersect_combinations_probabilities[idx_sort]
#     values, idx_start, count = np.unique(sorted_records_array, return_counts=True, return_index=True)
#     values = values[count > 1]
#     res = np.split(idx_sort, idx_start[1:])
#     res = list(filter(lambda x: x.size > 1, res))[0]
#
#     intersect_combinations = intersect_combinations[res]
#     intersect_combinations = get_intersections(intersect_combinations)
#
#     if len(intersect_combinations) != 1:
#         raise Exception("Illegal state")
#     return {intersect_combinations[0]: values[0]}


def get_probable_strings(probabilistic_intersection: dict[str, float], str_count=1) -> list[str]:
    texts = list(probabilistic_intersection.keys())
    return texts[:str_count]


def get_probabilistic_intersection(sets: dict[str, int], length_bias=2.0, count_bias=1.0):
    texts = list(sets.keys())
    global_count = list(sets.values())

    substr = []
    substr_index = []

    for i, string in enumerate(texts):
        str_len = len(string)
        for j in range(str_len):
            for k in range(j + 1, str_len + 1):
                substr_index.append(i)
                substr.append(string[j:k])

    unique_substr, unique_substr_index, substr_counts = np.unique(substr, return_counts=True, return_index=True)
    unique_substr_len = np.char.str_len(unique_substr)
    base_probability = substr_counts / np.amax(substr_counts)

    weight_1 = unique_substr_len / np.amax(unique_substr_len)
    weight_1 **= length_bias
    base_probability *= weight_1

    average_count = np.average(global_count)
    global_count = np.array(global_count, dtype=np.float32) / average_count
    substr_index = np.array(substr_index)[unique_substr_index]
    weight_2 = global_count[substr_index]
    weight_2 **= count_bias
    base_probability *= weight_2

    base_probability -= np.amin(base_probability)
    base_probability /= np.amax(base_probability)

    ret = {
        combination: probability
        for combination, probability in
        zip(unique_substr, base_probability)
    }
    return dict(sorted(ret.items(), key=lambda item: item[1], reverse=True))


def get_full_string(sets: dict[str, int], probabilities: dict[str, float]):
    full_strings = list(sets.keys())
    all_strings = list(probabilities.keys())

    mask = np.array([i in full_strings for i in all_strings])
    keys = np.array(all_strings)[mask]

    return {
        key: probabilities[key]
        for key in keys
    }


def remove_single_chars(dictionary):
    keys = list(dictionary.keys())
    str_lengths = np.char.str_len(keys)
    indices = np.argwhere(str_lengths <= 1)
    keys = np.delete(keys, indices)
    return {
        key: value
        for key, value in zip(keys, list(dictionary.values()))
    }


def get_groups(sets: dict[str, int], fill_char='\\'):
    texts = [i for i in sets.keys()]
    str_lengths = np.char.str_len(texts)

    average_len = round(np.average(str_lengths))
    min_len, max_len = (average_len - 1, average_len + 1)
    mask = np.bitwise_and(max_len >= str_lengths, str_lengths >= min_len)
    texts = np.array(texts)[mask]

    str_lengths = np.char.str_len(texts)
    trailing_count = np.abs(str_lengths - max_len)
    trailing_chars = [''.join([fill_char for _ in range(i)]) for i in trailing_count]
    texts = [string + char for string, char in zip(texts, trailing_chars)]

    chars = np.array([[*i] for i in texts])
    group_1_key = chars[:, 0]
    unique_group_1, indices_group_1 = np.unique(group_1_key, return_inverse=True)
    group_count = unique_group_1.shape[0]
    group_1 = [[] for _ in range(group_count)]
    for i, string in zip(indices_group_1, chars):
        group_1[i].append(string)

    group_1_threshold = round(chars.shape[0] / group_count)
    group_1_lengths = [len(i) for i in group_1]
    mask = np.argwhere(np.array(group_1_lengths) < group_1_threshold).reshape(-1)
    group_1 = np.delete(group_1, mask)

    return [
        {(key := ''.join(j).replace(fill_char, "")): sets[key] for j in i}
        for i in group_1
    ]


def main():
    # print(get_probable_string(get_probabilistic_intersection_1({
    #     '黄冠道人': 1,
    #     '黄冠道': 1,
    # })))
    #
    # print(get_probable_string(get_probabilistic_intersection_1({
    #     '谢逊所授': 1,
    #     '谢逊所为': 1,
    #     '谢逊所杀': 1
    # })))
    #
    # print(get_probable_string(get_probabilistic_intersection_1({
    #     '杨不悔醒': 1,
    #     '杨不悔颈': 1,
    #     '杨不悔搂': 1,
    #     '杨不悔见': 1,
    #     '杨不悔来': 1,
    #     '杨不悔道': 1
    # })))
    #
    # print(get_probable_string(get_probabilistic_intersection_1({
    #     "龙姐姐": 23,
    #     "周姐姐": 24,
    #     "杨姐姐": 27,
    # })))
    #
    # print(get_probable_string(get_probabilistic_intersection_1({
    #     "abcde": 30,
    #     "febcde": 15,
    #     "bcdefgh": 2,
    #     "cd": 5
    # })))  # bcde
    #
    # print(get_probable_string(get_probabilistic_intersection_1({
    #     "abcd": 30,
    #     "bcde": 15,
    #     "bcd": 2,
    #     "cd": 5
    # })))  # bcd
    #
    # print(get_probable_string(get_probabilistic_intersection_1({
    #     "abcde": 30,
    #     "febcde": 15,
    #     "bcdefgh": 2,
    #     "cd": 5
    # })))  # bcde
    #
    # print(get_probable_string(get_probabilistic_intersection_1({
    #     "cd": 40,
    #     "abd": 40,
    #     "bd": 40
    # })))  # bd
    #
    # print(get_probable_string(get_probabilistic_intersection({
    #     "d": 40,
    #     "abd": 40,
    #     "bd": 40
    # })))  # bd
    #
    # print(get_probable_string(get_probabilistic_intersection({
    #     "cbd": 40,
    #     "ab": 40,
    #     "bd": 40
    # })))  # bd

    import pickle
    # with open("all_actors", "rb") as file:
    #     new_names = pickle.load(file)
    with open("names_3000", "rb") as file:
        new_names = pickle.load(file)

    # new_names = remove_single_chars(new_names)
    groups = get_groups(new_names)

    for group in groups:
        keys = list(group.keys())
        keys_ = [i[1:] for i in keys]
        leading_char = keys[0][0]
        group_ = {
            key: group[keys[i]]
            for i, key in enumerate(keys_)
        }

        probabilities = get_probabilistic_intersection(group_, length_bias=1.75, count_bias=1)
        a = get_full_string(group_, probabilities)
        print(f"{group}\n{[leading_char + i for i in get_probable_strings(a, str_count=2)]}\n")


if __name__ == '__main__':
    main()
