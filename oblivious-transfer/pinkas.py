import random

from charm.toolbox.ecgroup import ECGroup, ZR, G
from charm.toolbox.eccurve import prime192v1, prime256v1


class Pinkas:
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
        a['r'] = group.random(ZR)
        a['R'] = a['g'] ** a['r']
        a['C'] = [group.random(G) for _ in range(len(a['m']) - 1)]
        a['Cr'] = [C ** a['r'] for C in a['C']]
        return {'R': a['R'], 'C': a['C']}

    def choose(self, b):
        b['k'] = group.random(ZR)
        b['v'] = b['g'] ** b['k']

        if b['b'] > 0:
            b['v'] = b['C'][b['b'] - 1] / b['v']

        b['m'] = b['R'] ** b['k']
        return {'v': b['v']}

    def mask(self, a):
        a["m'"] = [a['v'] ** a['r']]
        a["m'"] += [Cr / a["m'"][0] for Cr in a['Cr']]
        return {"m'": a["m'"]}


if __name__ == "__main__":
    # Just testing
    OT = Pinkas(ECGroup(prime256v1))

    a, b = OT.gen_params()
    OT.gen_msgs(a, 1000)
    b.update({'b': 999})
    b.update(OT.setup(a))
    a.update(OT.choose(b))
    b.update(OT.mask(a))

    print(b["m"] == a["m'"][b["b"]])
