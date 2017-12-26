import random

from charm.core.math.integer import integer, random, randomPrime
from charm.schemes.pkenc.pkenc_rsa import RSA_Enc


class RSA:
    def __init__(self, key_size):
        self.key_size = key_size

    def gen_params(self):
        b, a = RSA_Enc().keygen(self.key_size)
        return a, b

    def gen_msgs(self, a, count):
        a['m'] = [random(a['N']) for _ in range(count)]

    def setup(self, a):
        a['x'] = [random(a['N']) for _ in a['m']]
        return {'x': a['x']}

    def choose(self, b):
        b['k'] = random(b['N'])
        b['v'] = b['x'][b['b']] + b['k'] ** b['e']
        b['m'] = b['k']
        return {'v': b['v']}

    def mask(self, a):
        a["m'"] = [(a['v'] - x) ** (a['d'] % a['phi_N']) for x in a['x']]
        return {"m'": a["m'"]}


if __name__ == "__main__":
    # Just testing
    OT = RSA(1024)

    a, b = OT.gen_params()
    OT.gen_msgs(a, 1000)
    b.update({'b': 2})
    b.update(OT.setup(a))
    a.update(OT.choose(b))
    b.update(OT.mask(a))

    print(b["m"] == a["m'"][b["b"]])
