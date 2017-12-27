from charm.toolbox.pairinggroup import PairingGroup, ZR, G1, G2, GT, pair


class OkamotoRom:
    def __init__(self, group_obj):
        global group
        group = group_obj

    def commit(self, p):
        """ Prover -- Commit """
        p['r'] = [group.random(ZR) for _ in range(2)]
        p['X'] = p['g'][0] ** p['r'][0] * p['g'][1] ** p['r'][1]
        return {'X': p['X']}

    def challenge(self, v):
        """ Verifier -- Challenge """
        v['c'] = group.random(ZR)
        return {'c': v['c']}

    def answer(self, p):
        """ Prover -- Answer Challange """
        p['gd'] = group.hash(group.serialize(p['X']) + group.serialize(p['c']), G1)
        p['s'] = [p['gd'] ** (r + sk * p['c']) for r, sk in zip(p['r'], p['sk'])]
        return {'s': p['s']}

    def verify(self, v):
        """ Verifier --  Verify """
        v['gd'] = group.hash(group.serialize(v['X']) + group.serialize(v['c']), G1)

        lhs = pair(v['s'][0], v['g'][0]) * pair(v['s'][1], v['g'][1])
        rhs = pair(v['gd'], v['pk'] ** v['c'] * v['X'])

        return lhs == rhs

def test():
    # Just testing

    G = PairingGroup('MNT224')
    IDS = OkamotoRom(G)

    g = [G.random(G2), G.random(G2)]
    sk = G.random(ZR, 2)
    pk = g[0] ** sk[0] * g[1] ** sk[1]

    p = {'sk': sk, 'g': g}
    v = {'pk': pk, 'g': g}

    v.update(IDS.commit(p))
    p.update(IDS.challenge(v))
    v.update(IDS.answer(p))
    print(IDS.verify(v))

if __name__ == "__main__":
    test()
