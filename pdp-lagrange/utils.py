from functools import reduce


class Poly:
    def __init__(self, coeffs):
        self.coeffs = coeffs

    def __len__(self):
        return len(self.coeffs)

    def __getitem__(self, i):
        return self.coeffs[i]

    def __setitem__(self, i, value):
        self.coeffs[i] = value

    def __call__(self, x):
        return reduce(lambda acc, a: acc * x + a, reversed(self.coeffs))


def product(A):
    return reduce(lambda x, y: x * y, A)
