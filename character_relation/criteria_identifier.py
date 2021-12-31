import pickle


def main():
    with open("data/criteria_data", "rb") as file:
        data = pickle.load(file)
    words = data["words"]
    one_hot_softmax = data["one_hot_softmax"]
    indices = data["indices"]
    vectors = data["vectors"]

    print()


if __name__ == '__main__':
    main()
