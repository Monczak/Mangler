from functools import wraps


class GeneratorWrapper:
    def __init__(self, gen):
        self._gen = gen
        self._count = 0

    @property
    def next(self):
        self._count += 1
        return next(self._gen)

    @property
    def count(self):
        return self._count


class ValueKeepingGenerator:
    def __init__(self, gen):
        self._gen = gen
        self.value = None

    def __iter__(self):
        self.value = yield from self._gen


def keep_value(fun):
    def wrapper(*args, **kwargs):
        return ValueKeepingGenerator(fun(*args, **kwargs))
    return wrapper
