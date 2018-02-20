from functools import reduce


def product(A):
    return reduce(lambda x, y: x * y, A)
