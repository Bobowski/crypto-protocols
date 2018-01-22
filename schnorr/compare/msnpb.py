import time

from charm.toolbox.pairinggroup import PairingGroup, ZR, G1, G2, GT, pair

G = PairingGroup('MNT159')


def step_0(p):
    """ Prover -- Commit """
    p['x'] = G.random(ZR)
    p['X'] = p['g'] ** p['x']
    return {'X': p['X']}

def step_1(v):
    """ Verifier -- Challange """
    v['c'] = G.random(ZR)
    v['r'] = G.random(ZR)
    v['gr'] = v['g'] ** v['r']
    return {'c': v['c'], 'gr': v['gr']}

def step_2(p):
    """ Prover -- Answer Challange """
    p['S'] = p['gr'] ** (p['sk'] * p['c'] + p['x'])
    return {'S': p['S']}

def step_3(v):
    """ Verifier --  Verify """
    accept = v['S'] == (v['pk'] ** v['c'] * v['X']) ** v['r']
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
