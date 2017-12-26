import random

from charm.toolbox.ecgroup import ECGroup, ZR, G
from charm.toolbox.eccurve import prime192v1, prime256v1


class DHSimple:
    def __init__(self, group_obj):
        global group
        group = group_obj

    def gen_params(self):
        g = group.random(G)
        a = {'g': g}
        b = {'g': g}
        return a, b

    def gen_msgs(self, a, count):
        a['m'] = [group.random(G) for _ in range(count)]

    def setup(self, a):
        a['a'] = group.random(ZR)
        a['A'] = a['g'] ** a['a']
        a['A2'] = a['A'] ** a['a']
        a['A3'] = [a['A2'] ** i for i in range(1, len(a['m']))]
        return {'A': a['A']}

    def choose(self, b):
        b['k'] = group.random(ZR)
        b['v'] = (b['A'] ** b['b']) * (b['g'] ** b['k'])
        b['m'] = b['A'] ** b['k']
        return {"v": b['v']}

    def mask(self, a):
        a["m'"] = [a['v'] ** a['a']]
        a["m'"] += [a["m'"][0] / A3 for A3 in a['A3']]
        # a["m'"] += [a['v'] ** a['a'] / a['A2'] ** i for i in range(1, len(a['m']))]
        return {"m'": a["m'"]}


if __name__ == "__main__":
    # Just testing
    OT = DHSimple(ECGroup(prime256v1))

    a, b = OT.gen_params()
    OT.gen_msgs(a, 55)
    b.update({'b': 42})
    b.update(OT.setup(a))
    a.update(OT.choose(b))
    b.update(OT.mask(a))

    print(b["m"] == a["m'"][b["b"]])
