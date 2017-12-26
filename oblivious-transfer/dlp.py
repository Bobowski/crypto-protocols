import random

from charm.toolbox.ecgroup import ECGroup, ZR, G
from charm.toolbox.eccurve import prime192v1, prime256v1


class DLP:
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
        a['r'] = [group.random(ZR) for _ in range(len(a['m']))]
        a['r-1'] = [r ** -1 for r in a['r']]
        a['R'] = [a['g'] ** r for r in a['r']]
        return {'R': a['R']}

    def choose(self, b):
        b['k'] = group.random(ZR)
        b['v'] = b['R'][b['b']] ** b['k']
        b['m'] = b['g'] ** b['k']
        return {'v': b['v']}

    def mask(self, a):
        a["m'"] = [a['v'] ** r1 for r1 in a['r-1']]
        return {"m'": a["m'"]}


if __name__ == "__main__":
    # Just testing
    OT = DLP(ECGroup(prime256v1))

    a, b = OT.gen_params()
    OT.gen_msgs(a, 1000)
    b.update({'b': 2})
    b.update(OT.setup(a))
    a.update(OT.choose(b))
    b.update(OT.mask(a))

    print(b["m"] == a["m'"][b["b"]])
