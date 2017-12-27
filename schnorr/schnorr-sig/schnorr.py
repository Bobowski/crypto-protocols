from charm.toolbox.pairinggroup import PairingGroup, ZR, G1, G2, GT, pair

G = PairingGroup('SS512')


def step_0(s):
    """ Signer -- sign """
    s['r'] = G.random(ZR)
    s['R'] = s['g'] ** s['r']
    s['h'] = G.hash(G.serialize(s['R']) + G.serialize(s['m']))
    s['s'] = s['r'] + s['sk'] * s['h']
    return {'R': s['R'], 's': s['s']}

def step_1(v):
    v['h'] = G.hash(G.serialize(v['R']) + G.serialize(v['m']))
    accept = v['g'] ** v['s'] == v['R'] * v['pk'] ** v['h']
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
