from charm.toolbox.pairinggroup import PairingGroup, ZR, G1, G2, GT, pair


class OkamotoStd:
    def __init__(self, group_obj):
        global group
        group = group_obj

    def commit(self, p):
        """ Prover -- Commit """
        p['r'] = [group.random(ZR) for _ in range(2)]
        p['X'] = p['g'][0] ** p['r'][0] * p['g'][1] ** p['r'][1]
        return {'X': p['X']}

    def challenge(self, v):
        """ Verifier -- Challange """
        v['c'] = group.random(ZR)
        return {'c': v['c']}

    def answer(self, p):
        """ Prover -- Answer Challange """
        p['s'] = [r + sk * p['c'] for r, sk in zip(p['r'], p['sk'])]
        return {'s': p['s']}

    def verify(self, v):
        """ Verifier --  Verify """
        lhs = v['g'][0] ** v['s'][0] * v['g'][1] ** v['s'][1]
        rhs = v['pk'] ** v['c'] * v['X']
        return lhs == rhs


def test():
    # Just testing
    G = PairingGroup('SS512')
    IDS = OkamotoStd(G)

    g = G.random(G1, 2)
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
