import random

from charm.core.math.integer import integer, random, randomPrime
from charm.schemes.pkenc.pkenc_rsa import RSA_Enc

from utils import product

# RSA OBLIVIOUS TRANSFER 1-of-N

def step_0(a):
    a['x'] = [random(a['N']) for _ in a['m']]
    return {'x': a['x']}

def step_1(b):
    b['k'] = random(b['N'])
    b['v'] = b['x'][b['b']] + b['k'] ** b['e']
    return {'v': b['v']}

def step_2(a):
    a['k'] = [(a['v'] - x) ** (a['d'] % a['phi_N']) for x in a['x']]
    a["m'"] = [m + k for m, k in zip(a['m'], a['k'])]
    return {"m'": a["m'"]}

def step_3(b):
    b["m"] = b["m'"][b['b']] - b['k']
    return {"m": b["m"]}


if __name__ == "__main__":
    # Just testing
    b, a = RSA_Enc().keygen(512)
    m = [random(a['N']) for _ in range(10)]
    a.update({"m": m})
    b.update({"b": 0})

    b.update(step_0(a))
    a.update(step_1(b))
    b.update(step_2(a))
    step_3(b)
    print(b["m"] == a["m"][b["b"]])
