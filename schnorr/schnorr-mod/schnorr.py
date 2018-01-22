from charm.toolbox.pairinggroup import PairingGroup, ZR, G1, G2, GT, pair

G = PairingGroup('SS512')


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
    p['gd'] = G.hash(G.serialize(p['X']) + G.serialize(p['c']), G1)
    p['s'] = p['gd'] ** (p['sk'] * p['c'] + p['r'])
    return {'s': p['s']}

def step_3(v):
    """ Verifier --  Verify """
    v['gd'] = G.hash(G.serialize(v['X']) + G.serialize(v['c']), G1)
    accept = pair(v['s'], v['g']) == pair(v['gd'], v['X'] * v['pk'] ** v['c'])
    return {"Accept": accept}


if __name__ == "__main__":
    # Just testing
    g = G.random(G1)
    sk = G.random(ZR)
    pk = g ** sk

    p = {'sk': sk, 'g': g}
    v = {'pk': pk, 'g': g}

    v.update(step_0(p))
    p.update(step_1(v))
    v.update(step_2(p))
    print(step_3(v))
