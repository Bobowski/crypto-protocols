import time

from charm.toolbox.pairinggroup import PairingGroup, ZR, G1, G2, GT, pair

G = PairingGroup('MNT159')


def step_0(p):
    """ Prover -- Commit """
    p['r'] = G.random(ZR)
    p['X'] = p['g'] ** p['r']
    return {'X': p['X']}

def step_1(v):
    """ Verifier -- Challange """
    v['c'] = G.random(ZR)
    return {'c': v['c']}

def step_2(p):
    """ Prover -- Answer Challange """
    p['s'] = p['sk'] * p['c'] + p['r']
    return {'s': p['s']}

def step_3(v):
    """ Verifier --  Verify """
    accept = v['g'] ** v['s'] == v['pk'] ** v['c'] * v['X']
    return {"Accept": accept}


if __name__ == "__main__":
    # Just testing
    g = G.random(G1)
    sk = G.random(ZR)
    pk = g ** sk

    p = {'sk': sk, 'g': g}
    v = {'pk': pk, 'g': g}

    t = time.time()
    for i in range(2500):
        v.update(step_0(p))
        p.update(step_1(v))
        v.update(step_2(p))
        val = step_3(v)
    t = time.time() - t
    print(val, t, t / 2500)
