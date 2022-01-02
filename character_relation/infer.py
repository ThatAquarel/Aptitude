from tensorflow import keras

from character_relation.model import CharacterRelationModel

model = CharacterRelationModel()

keras_model = keras.models.load_model("character_relation_model")

test_sentences = [
    "My boss at work is extremely toxic, he insults everyone.",
    "He's my accomplice.",
    "He's my rival in a swimming competition",
    "Romeo and Juliet, the two secret lovers of the Shakespeare era.",
    "The love and hate relationship that I have with her.",
    "My coworker and I work very efficiently together.",
    "He's so boring and always has a serious tone.",
    "A social media influencer has many attracted and dedicated fans.",
    "They kissed in front of everyone at a party."
]
y = keras_model.predict(model.preprocess(test_sentences))
print(y)
