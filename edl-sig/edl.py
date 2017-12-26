from charm.toolbox.pairinggroup import PairingGroup, ZR, G1, G2, GT, pair

G = PairingGroup('SS512')


def step_0(s):
    """ Signer -- sign """
    s['r'] = G.random(ZR)
    s['h'] = G.hash(G.serialize(s['m']) + G.serialize(s['r']), G1)
    s['z'] = s['h'] ** s['sk']

    s['k'] = G.random(ZR)
    s['u'] = s['g'] ** s['k']
    s['v'] = s['h'] ** s['k']
    s['c'] = G.hash(
        G.serialize(s['g']) +
        G.serialize(s['h']) +
        G.serialize(s['pk']) +
        G.serialize(s['z']) +
        G.serialize(s['u']) +
        G.serialize(s['v'])
    )
    s['s'] = s['k'] + s['c'] * s['sk']

    return {'z': s['z'], 'r': s['r'], 's': s['s'], 'c': s['c']}

def step_1(v):
    """ Verifier -- verify """
    v['h'] = G.hash(G.serialize(v['m']) + G.serialize(v['r']), G1)
    v['u'] = v['g'] ** v['s'] * v['pk'] ** (-v['c'])
    v['v'] = v['h'] ** v['s'] * v['z'] ** (-v['c'])

    v["c'"] = G.hash(
        G.serialize(v['g']) +
        G.serialize(v['h']) +
        G.serialize(v['pk']) +
        G.serialize(v['z']) +
        G.serialize(v['u']) +
        G.serialize(v['v'])
    )
    return v['c'] == v["c'"]

def main():
    # Just testing
    g = G.random(G1)
    m = G.random(ZR)
    sk = G.random(ZR)
    pk = g ** sk

    s = {'sk': sk, 'pk': pk, 'g': g, 'm': m}
    v = {'pk': pk, 'g': g, 'm': m}

    v.update(step_0(s))
    print(step_1(v))

if __name__ == "__main__":
    main()
