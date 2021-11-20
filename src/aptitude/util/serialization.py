import pickle


# import hmac
# import hashlib
# from inspect import getsource


# def get_class_hash(instance, data) -> str:
#     key = hashlib.sha256(getsource(instance.__class__).encode("utf-8")).digest()
#     return hmac.new(key, data, digestmod=hashlib.sha256).hexdigest()
#
#
# def write_hash(class_name, class_hash):
#     file = parse_hashes()
#     for i, line in enumerate(file):
#         name_, _ = line
#
#         if name_ == class_name:
#             file[i][1] = class_hash
#
#
#
#
# def write_hashes(file: list[list[str, str]]):
#     with open("aptitude_hashes.csv", "w+") as file:
#         for line in file:
#
#
#         "_".join(i for i in ["class", "hash"])
#
#         file.write()
#
# def parse_hashes() -> list[list[str, str]]:
#     with open("aptitude_hashes.csv", "r") as file:
#         return [line.split(",") for line in file.readlines()]


def serialized_cache(function):
    def wrapper(*args, **kwargs):
        instance = args[0]
        if not isinstance(instance, object):
            raise TypeError("@serialize must decorate class method")
        class_name = instance.__class__.__name__

        try:
            with open(f"{class_name}.aptitude", "rb+") as file:
                return pickle.load(file)

        except FileNotFoundError:
            data = function(*args, **kwargs)
            if data is None:
                raise TypeError("Decorated method must return data")

            with open(f"{class_name}.aptitude", "wb+") as file:
                pickle.dump(data, file)

            return data

        # serialized_hash = get_class_hash(instance, data)
        # with open("aptitude_hashes.csv", "a+") as file:
        #     file.write(f"{class_name},{serialized_hash}")

    return wrapper
