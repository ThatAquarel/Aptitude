import spacy
import numpy as np

# nlp = spacy.load("en_core_web_lg")
# doc = nlp("Alex sees a photo in which one handsome boy, Benjamin, plays football.")
nlp = spacy.load("zh_core_web_lg")
doc = nlp("他在这雪谷幽居，至此时已五年有余，从一个孩子长成为身材高大的青年。")

tokens = np.array([token for token in doc])
mask_0 = [token.is_punct for token in tokens]
mask_1 = [token.pos_ in ['DET', 'ADP'] for token in tokens]
mask = np.invert(np.bitwise_or(mask_0, mask_1))
tokens = tokens[mask]

root_deps = [list(token.ancestors) for token in tokens]
root_deps_len = np.array([len(dep) for dep in root_deps])

max_root_deps_len = np.amax(root_deps_len)
indices = []
for i in range(max_root_deps_len):
    j = i + 1

    a = root_deps_len[:-2] == j
    b = root_deps_len[1:-1] == i
    c = root_deps_len[2:] == j

    indices.extend(np.argwhere(a & b & c).reshape(-1).tolist())

indices = np.array(indices)
subj = tokens[indices]
conj = tokens[indices + 1]
objc = tokens[indices + 2]

print(np.concatenate((subj[:, None], conj[:, None], objc[:, None]), axis=1))
