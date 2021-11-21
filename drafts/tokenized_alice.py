import re

import spacy

with open("../books/alice_in_wonderland.txt", "r") as file:
    text = file.read()

texts = re.split("[.?!]", text)
texts = [text.replace("\n", " ") for text in texts]

nlp = spacy.load('en_core_web_md')
docs = list(nlp.pipe(texts))

with open("tokenized_alice.txt", "w+") as file:
    for doc in docs:
        for token in doc:
            text = [token.text, token.dep_, token.pos_, token.head.text, token.head.pos_, ]
            text.extend([child for child in token.children])
            text = [str(token).replace("\n", " ") for token in text]

            file.write(f"{' '.join(text)}\n")
