import spacy
from spacy.matcher import DependencyMatcher
import re

with open("../books/alice_in_wonderland.txt", "r") as file:
    text = file.read()

texts = re.split("[.?!]", text)

nlp = spacy.load("en_core_web_trf")
entity = 'Alice'
docs = list(nlp.pipe(texts))
matcher = DependencyMatcher(nlp.vocab)

pattern = [
    {
        "RIGHT_ID": "anchor_entity",
        "RIGHT_ATTRS": {"ORTH": entity}
    },
    {
        "LEFT_ID": "anchor_entity",
        "REL_OP": "<<",
        "RIGHT_ID": "root",
        "RIGHT_ATTRS": {'DEP': 'ROOT'}
    },
    {
        "LEFT_ID": "root",
        "REL_OP": ">>",
        "RIGHT_ID": "subject",
        "RIGHT_ATTRS": {'DEP': 'nsubj'}
    }
]

matcher.add("bingyu_dobj_path", [pattern])
for doc in docs:
    matches = matcher(doc)
    if len(matches) == 0:
        continue
    match_id, token_ids = matches[0]

    for match in token_ids:
        print(doc[match])
