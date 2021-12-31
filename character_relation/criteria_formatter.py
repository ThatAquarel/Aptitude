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
    "friend",
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
    "unsympathetic",
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
    "superior",
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
    # nlp = spacy.load("en_core_web_md")
    # criteria = np.array([
    #     [introvert, extrovert],
    #     [positive, negative],
    #     [superior, inferior],
    #     [personal, professional],
    #     [emotional, indifferent]
    # ], dtype=list)
    #
    # criteria_vec = np.empty(criteria.shape, dtype=list)
    # for i, x in enumerate(criteria):
    #     for j, y in enumerate(x):
    #         criteria_vec[i, j] = [i.vector for i in nlp.pipe(y) if i.has_vector]
    #
    # len_c = [len(i) for i in criteria.reshape(-1)]
    # len_cv = [len(i) for i in criteria_vec.reshape(-1)]
    # if len_c != len_cv:
    #     raise Exception("Some words of criteria don't have word vectors")
    #
    # with open("criteria_vectors", "wb") as file:
    #     pickle.dump(criteria_vec, file)

    criteria = [
        [extrovert, introvert],
        [positive, negative],
        [superior, inferior],
        [personal, professional],
        [emotional, indifferent]
    ]

    for criterion in criteria:
        print("{")
        for i, a in enumerate(criterion):
            for b in a:
                c = 1
                if i == 1:
                    c = -1
                print(f"\"{b}\":{c},")
        print("}")


if __name__ == '__main__':
    main()
