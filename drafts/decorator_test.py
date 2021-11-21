import inspect
import hashlib

def decorator_test(function):
    def wrapper(*args, **kwargs):
        return function(*args, **kwargs)

    return wrapper


class Test:
    @decorator_test
    def test(self, x):
        print(x)


Test().test("aaa")
