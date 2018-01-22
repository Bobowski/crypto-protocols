from functools import reduce

from charm.core.math.integer import reduce as reduce_int

import hashlib


def ID(f):
    """ Helper function to calculate ID(f) """
    return hashlib.sha1(str(f).encode('utf-8')).hexdigest()


class Poly:
    """ Polynomial class for simpler representation of operations """
    def __init__(self, coeffs):
        self.coeffs = list(coeffs)

    def __len__(self):
        return len(self.coeffs)

    def __getitem__(self, i):
        return self.coeffs[i]

    def __setitem__(self, i, value):
        self.coeffs[i] = value

    def __call__(self, x):
        return reduce_int(reduce(lambda acc, a: acc * x + a, reversed(self.coeffs)))


def product(A):
    return reduce(lambda x, y: x * y, A)

def sum(A):
    return reduce(lambda x, y: x + y, A)

def LIexp(phi, xc):
    """ Calculate LIexp for elements phi in point xc """
    return product(
        grLx ** product((xc - mj) / (m - mj) for mj, _ in phi if mj != m)
        for m, grLx in phi
    )

def LI(points, xc):
    return reduce_int(sum([
        yj * product([(xc - xm) / (xj - xm) for xm, _ in points if xm != xj])
        for xj, yj in points
    ]))
