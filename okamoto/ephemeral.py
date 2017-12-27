from charm.toolbox.pairinggroup import PairingGroup, ZR, G1, G2, GT, pair

from utils import product

G = PairingGroup('SS512')


def step_0(p):
    """ Prover -- Commit """
    p['r'] = G.random(ZR, 2)
    p['X'] = product(g **  r for g, r in zip(p['g'], p['r']))
    return {'X': p['X']}

def step_1(v):
    """ Verifier -- Challange """
    v['c'] = G.random(ZR)
    v['r'] = G.random(ZR)
    v['gd'] = [g ** v['r'] for g in v['g']]
    return {'c': v['c'], 'gd': v['gd']}

def step_2(p):
    """ Prover -- Answer Challange """
    p['s'] = [g ** (r + sk * p['c']) for r, sk, g in zip(p['r'], p['sk'], p['gd'])]
    return {'s': p['s']}

def step_3(v):
    """ Verifier --  Verify """
    lhs = product(v['s'])
    rhs = v['pk'] ** (v['c'] * v['r']) * v['X'] ** v['r']
    accept = lhs == rhs
    return {"Accept": accept}


if __name__ == "__main__":
    # Just testing
    g = G.random(G1, 2)
    sk = G.random(ZR, 2)
    pk = product(g_ ** sk for g_, sk in zip(g, sk))

    p = {'sk': sk, 'g': g}
    v = {'pk': pk, 'g': g}

    v.update(step_0(p))
    p.update(step_1(v))
    v.update(step_2(p))
    print(step_3(v))
