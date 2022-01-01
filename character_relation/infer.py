from tensorflow import keras

from character_relation.model import CharacterRelationModel

model = CharacterRelationModel()

keras_model = keras.models.load_model("character_relation_model")
y = keras_model.predict(model.preprocess([
    "My boss at work is extremely toxic, he insults everyone.",
    "He's my accomplice",
    "He's my rival in a swimming competition"
]))

print(y)
