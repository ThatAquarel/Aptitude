import pickle

from tensorflow import keras

from character_relation.model import CharacterRelationModel


def main():
    model = CharacterRelationModel.get_model()
    model.build()
    print(model.summary())

    model.compile(loss=keras.losses.BinaryCrossentropy(from_logits=True),
                  optimizer=keras.optimizers.Adam(1e-4),
                  metrics=['accuracy'])

    with open("data/dataset", "rb") as file:
        dataset = pickle.load(file)
    model.fit(x=dataset['x'], y=dataset['y'], batch_size=64, epochs=128, validation_split=0.2)

    model.save("character_relation_model")


if __name__ == '__main__':
    main()