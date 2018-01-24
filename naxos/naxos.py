from charm.toolbox.pairinggroup import PairingGroup, ZR, G1, G2, GT, pair

G = PairingGroup('SS512')

def step_0(a):
    a['esk'] = G.random(ZR)
    a['X'] = a['g'] ** G.hash(G.serialize(a['esk']) + G.serialize(a['a']), ZR)
    return {'X': a['X']}

def step_1(b):
    b['esk'] = G.random(ZR)
    b['Y'] = b['g'] ** G.hash(G.serialize(b['esk']) + G.serialize(b['b']), ZR)

    a1 = b['A'] ** G.hash(G.serialize(b['esk']) + G.serialize(b['b']), ZR)
    a2 = b['X'] ** b['b']
    a3 = b['X'] ** G.hash(G.serialize(b['esk']) + G.serialize(b['b']), ZR)

    b['K'] = G.hash(
        G.serialize(a1) +
        G.serialize(a2) +
        G.serialize(a3) +
        G.serialize(b['A']) +
        G.serialize(b['B'])
        , ZR
    )
    return {'Y': b['Y']}

def step_2(a):
    a1 = a['Y'] ** a['a']
    a2 = a['B'] ** G.hash(G.serialize(a['esk']) + G.serialize(a['a']), ZR)
    a3 = a['Y'] ** G.hash(G.serialize(a['esk']) + G.serialize(a['a']), ZR)

    a['K'] = G.hash(
        G.serialize(a1) +
        G.serialize(a2) +
        G.serialize(a3) +
        G.serialize(a['A']) +
        G.serialize(a['B'])
        , ZR
    )


def main():
    # Just testing
    g = G.random(G1)
    sk_a = G.random(ZR)
    pk_a = g ** sk_a
    sk_b = G.random(ZR)
    pk_b = g ** sk_b
    a = {'g': g, 'a': sk_a, 'A': pk_a, 'B': pk_b}
    b = {'g': g, 'b': sk_b, 'B': pk_b, 'A': pk_a}

    b.update(step_0(a))
    a.update(step_1(b))
    step_2(a)

    print(a['K'] == b['K'])

if __name__ == "__main__":
    main()
