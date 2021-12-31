introvert = [
    "introvert",
    "solitary",
    "loner",
    "thinker",
    "homebody",
    "reserved"
]
extrovert = [
    "extrovert",
    "outgoing",
    "congenial",
    "gregarious",
    "personable",
    "sociable",
    "cordial",
    "demonstrative",
    "friendly",
    "social",
    "unreserved"
]

positive = [
    "ally",
    "associate",
    "colleague",
    "partner",
    "accessory",
    "accomplice",
    "co-worker",
    "coadjutor",
    "collaborator",
    "confederate",
    "helper",
    "peer",
    "wife",
    "husband",
    "spouse",
    "chum",
    "pal",
    "mate",
    "teammate",
    "coworker",
    "advocate",
    "backer",
    "patron",
    "supporter"
]
negative = [
    "rival",
    "adversary",
    "challenger",
    "competition",
    "competitor",
    "contender",
    "opponent",
    "antagonist",
    "contestant",
    "emulator",
    "entrant",
    "equal",
    "equivalent",
    "match",
    "opposite",
    "outplay",
    "outrun",
    "overcome",
    "overtake",
    "overwhelm",
    "top",
    "triumph",
    "whip",
    "best",
    "better",
    "conquer",
    "exceed",
    "excel",
    "outdo",
    "outshine",
    "outstrip",
    "subdue",
    "transcend",
    "vanquish",
    "victorious"
]

superior = [
    "superior",
    "boss",
    "manager",
    "principal",
    "ruler",
    "supervisor",
    "CEO",
    "VIP",
    "brass",
    "chief",
    "chieftain",
    "director",
    "elder",
    "exec",
    "executive",
    "head",
    "heavyweight",
    "higher-up",
    "leader",
    "senior"
]
inferior = [
    "inferior",
    "adherent",
    "attendant",
    "auxiliary",
    "deputy",
    "disciple",
    "follower",
    "hanger-on",
    "hireling",
    "junior",
    "menial",
    "minion",
    "minor",
    "pawn",
    "satellite",
    "subaltern",
    "subject",
    "subordinate",
    "sycophant",
    "underling",
    "servant",
    "domestic"
]

personal = [
    "friend",
    "relative",
    "aunt",
    "cousin",
    "father",
    "folk",
    "mother",
    "niece",
    "sibling",
    "uncle",
    "blood",
    "brother-in-law",
    "cognate",
    "connection",
    "father-in-law",
    "folks",
    "grandparents",
    "in-laws",
    "mother-in-law",
    "nephew",
    "relation",
    "sister-in-law",
    "stepbrother",
    "stepparent",
    "stepsister",
    "great-grandparents"
]
professional = [
    "professionalism",
    "civility",
    "expertise",
    "rectitude",
    "respectability",
    "competence",
    "probity",
    "steadiness",
    "thoroughness",
    "acumen",
    "dedication",
    "facility",
    "reliability",
    "sophistication",
    "willingness",
    "independent",
    "disciplined",
    "organized",
    "proactive",
    "efficient",
    "resourceful",
    "meticulous",
    "consistent",
    "observant"
]

emotional = [
    "emotion",
    "affection",
    "love",
    "anger",
    "concern",
    "desire",
    "despair",
    "empathy",
    "excitement",
    "feeling",
    "fervor",
    "grief",
    "happiness",
    "joy",
    "passion",
    "pride",
    "rage",
    "remorse",
    "sadness",
    "sentiment",
    "shame",
    "sorrow",
    "sympathy",
    "warmth",
    "affect",
    "agitation",
    "ardor",
    "commotion",
    "despondency",
    "disturbance",
    "drive",
    "ecstasy",
    "elation",
    "excitability",
    "inspiration",
    "melancholy",
    "perturbation",
    "responsiveness",
    "satisfaction",
    "sensation",
    "sensibility",
    "sensitiveness",
    "thrill",
    "tremor",
    "vehemence",
    "vibes",
    "zeal"
]
indifferent = [
    "indifferent",
    "insensitive",
    "unsympathetic",
    "aloof",
    "apathetic",
    "callous",
    "detached",
    "diffident",
    "disinterested",
    "distant",
    "haughty",
    "heartless",
    "impartial",
    "impervious",
    "inattentive",
    "neutral",
    "nonchalant",
    "uncaring",
    "unconcerned",
    "uninvolved",
    "unresponsive",
    "cold",
    "cool",
    "dispassionate",
    "equitable",
    "heedless",
    "highbrow",
    "listless",
    "nonpartisan",
    "objective",
    "passionless",
    "phlegmatic",
    "regardless",
    "scornful",
    "silent",
    "stoical",
    "supercilious",
    "unaroused",
    "unbiased",
    "uncommunicative",
    "unemotional",
    "unimpressed",
    "unmoved",
    "unprejudiced",
    "unsocial"
]


def main():
    import spacy
    import pickle
    import numpy as np

    criteria = np.array([
        [extrovert, introvert],
        [positive, negative],
        [superior, inferior],
        [personal, professional],
        [emotional, indifferent]
    ], dtype=list)

    words = [word for word_set in np.reshape(criteria, -1) for word in word_set]
    softmax_shape = (len(words), len(criteria), 2)
    one_hot_softmax = np.zeros(softmax_shape, dtype=np.float32)
    indices = np.zeros((softmax_shape[0], 2), dtype=np.float32)

    idx = 0
    for i, criterion in enumerate(criteria):
        for j, word_set in enumerate(criterion):
            for _ in word_set:
                one_hot_softmax[idx, i, j] = 1
                indices[idx] = [i, j]
                idx += 1

    nlp = spacy.load("en_core_web_md")
    docs = list(nlp.pipe(words))
    vectors = np.array([doc.vector for doc in docs])

    data = {
        "words": words,
        "one_hot_softmax": one_hot_softmax,
        "indices": indices,
        "vectors": vectors
    }

    with open("criteria_data", "wb") as file:
        pickle.dump(data, file)


if __name__ == '__main__':
    main()
