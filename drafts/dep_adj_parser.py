import spacy
import numpy as np


def print_3_part_clause(doc):
    tokens = np.array([token for token in doc])
    mask_0 = [token.is_punct for token in tokens]
    # mask_1 = [token.pos_ in ['DET', 'ADP'] for token in tokens]
    # mask = np.invert(np.bitwise_or(mask_0, mask_1))
    tokens = tokens[np.invert(mask_0)]

    root_deps = [list(token.ancestors) for token in tokens]
    root_deps_len = np.array([len(dep) for dep in root_deps])

    root_deps_0 = [dep[0] if dep else None for dep in root_deps]
    unique_root_deps, inverse_idx = np.unique(root_deps_0, return_inverse=True)

    groups = [[] for _ in range(len(unique_root_deps))]
    for i, token in zip(inverse_idx, tokens):
        groups[i].append(token)
    len_groups = np.array([len(group) for group in groups])
    groups = np.delete(np.array(groups, dtype=list), np.where(len_groups == 1))

    # group some sibling tokens that are directly next to each other
    groups_idx = [[token.i for token in group] for group in groups]
    direct_siblings_groups = [[] for _ in range(len(groups))]
    for i, tokens_idx in enumerate(groups_idx):
        a = np.subtract(tokens_idx, np.arange(len(tokens_idx)))
        unique_a, inv_idx_a = np.unique(a, return_inverse=True)
        if unique_a.shape[0] == 1:
            continue
        direct_siblings_groups[i] = [[] for _ in range(len(unique_a))]
        for k, j in enumerate(inv_idx_a):
            direct_siblings_groups[i][j].append(groups[i][k])

    # remove det and adp
    direct_siblings_groups = [[[
        token for token in token_group
        if token.pos_ not in ['DET', 'ADP']
    ] for token_group in group
    ] for group in direct_siblings_groups]
    direct_siblings_groups = [[
        token_group for token_group in group if token_group
    ] for group in direct_siblings_groups]

    # get 3 part clauses
    direct_siblings_groups = [
        group[:2 - len(group)]
        if len(group) > 2 else group
        for group in direct_siblings_groups
        if group
    ]
    ancestors = [
        list(group[0][0].ancestors)[0]
        for group in direct_siblings_groups
    ]

    for group, ancestor in zip(direct_siblings_groups, ancestors):
        if ancestor.pos_ != "VERB":
            continue
        print(f"{group[0]} {ancestor} {group[1]}")

    # # get the current unique ancestors and remove them from the token groups
    # ancestors = []
    # for group in direct_siblings_groups:
    #     for token_group in group:
    #         # for token in token_group:
    #         ancestors.extend(list(token_group[0].ancestors))
    # ancestors = np.unique(ancestors)


def main():
    # nlp = spacy.load("en_core_web_lg")
    # doc = nlp("Alex sees a photo in which one handsome boy, Benjamin, plays football.")
    nlp = spacy.load("zh_core_web_lg")
    doc = nlp("他在这雪谷幽居，至此时已五年有余，从一个孩子长成为身材高大的青年。")
    print_3_part_clause(doc)

    print()
    doc = nlp("张无忌心中思潮起伏：“看来明教这一教派，中间包藏着许多原委曲折，并非单是专做坏事而已")
    print_3_part_clause(doc)

    print()
    doc = nlp("他自幼生长在父母和义父的慈爱卵翼之下，不懂得人间竟有心怀恶意的敌人。")
    print_3_part_clause(doc)

    print()
    doc = nlp("张无忌依法修练，练了两年有余，丹田中的氤氲紫气已有小成，可是体内寒毒胶固于经络百脉之中，非但无法化除，反而脸上的绿气日甚一日，"
              "每当寒毒发作，所受的煎熬也是一>日比一日更是厉害。")
    print_3_part_clause(doc)


if __name__ == '__main__':
    main()
