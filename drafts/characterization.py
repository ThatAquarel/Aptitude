import re

import spacy
from spacy.matcher import DependencyMatcher

with open("../books/alice_in_wonderland.txt", "r") as file:
    text = file.read()

texts = re.split("[.?!]", text)
texts = [text.replace("\n", " ") for text in texts]

# nlp = spacy.load("en_core_web_trf")
# nlp = spacy.load('en_core_web_md')
nlp = spacy.load('en_core_web_lg')
docs = list(nlp.pipe(texts))
matcher = DependencyMatcher(nlp.vocab)

# def render():
#     displacy.serve(doc)
#     time.sleep(1 << 32)
# thread = threading.Thread(target=render, args=(), daemon=True)
# thread.start()

pattern = [
    {
        "RIGHT_ID": "entity",
        "RIGHT_ATTRS": {"ORTH": "Alice"}
    },
    {
        "LEFT_ID": "entity",
        "REL_OP": "<<",
        "RIGHT_ID": "root",
        "RIGHT_ATTRS": {'DEP': 'ROOT'}
    },
    {
        "LEFT_ID": "root",
        "REL_OP": ">>",
        "RIGHT_ID": "adjectival_complement",
        "RIGHT_ATTRS": {'DEP': 'acomp'}
    },
    {
        "LEFT_ID": "root",
        "REL_OP": ">>",
        "RIGHT_ID": "clause_complement",
        "RIGHT_ATTRS": {'DEP': 'xcomp'}
    },
]
matcher.add("complements", [pattern])

for doc in docs:
    matches = matcher(doc)
    if len(matches) == 0:
        continue

    match_id, token_ids = matches[0]

    for match in token_ids:
        token = doc[match]

        if token.text != "Alice" and token.pos_ != "VERB":
            print(token)
