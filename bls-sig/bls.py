from charm.toolbox.pairinggroup import PairingGroup, ZR, G1, G2, GT, pair

G = PairingGroup('SS512')


def step_0(s):
    """ Signer -- sign """
    s['h'] = G.hash(G.serialize(s['m']), G1)
    s['s'] = s['h'] ** s['sk']
    return {'s': s['s']}

def step_1(v):
    v['h'] = G.hash(G.serialize(v['m']), G1)
    accept = pair(v['s'], v['g']) == pair(v['h'], v['pk'])
    return {"Accept": accept}


if __name__ == "__main__":
    # Just testing
    g = G.random(G1)
    m = G.random(ZR)
    sk = G.random(ZR)
    pk = g ** sk

    s = {'sk': sk, 'g': g, 'm': m}
    v = {'pk': pk, 'g': g, 'm': m}

    v.update(step_0(s))
    print(step_1(v))
