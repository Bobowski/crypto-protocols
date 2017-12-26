from charm.toolbox.pairinggroup import PairingGroup, ZR, G1, G2, GT, pair

G = PairingGroup('SS512')

def sign(m, sk):
    h = G.hash(G.serialize(m), G1)
    return h ** sk

def verify(m, sig, pk, g):
    h = G.hash(G.serialize(m), G1)
    return pair(sig, g) == pair(h, pk)

def MAC(m, sk):
    return G.hash(G.serialize(m) + G.serialize(sk))

def step_0(a):
    # Private / Public key
    a['a'] = G.random(ZR)
    a['A'] = a['g'] ** a['a']

    # Ephemeral value
    a['x'] = G.random(ZR)
    a['X'] = a['g'] ** a['x']
    return {'X': a['X']}

def step_1(b):
    # Private / Public key
    b['b'] = G.random(ZR)
    b['B'] = b['g'] ** b['b']

    # Ephemeral value
    b['y'] = G.random(ZR)
    b['Y'] = b['g'] ** b['y']

    # Shared secret
    b['K'] = b['X'] ** b['y']

    # Signatures
    b['SigB_X'] = sign(b['X'], b['b'])
    b['SigB_Y'] = sign(b['Y'], b['b'])

    # MAC
    b['MacK_B'] = MAC(b['B'], b['K'])

    return {
        'Y': b['Y'], 'B': b['B'],
        'SigB_X': b['SigB_X'], 'SigB_Y': b['SigB_Y'], 'MacK_B': b['MacK_B']
    }

def step_2(a):
    # Check SigB_X
    if not verify(a['X'], a['SigB_X'], a['B'], a['g']):
        print("FUCKUP AT SigB_X")
        return

    # Check SigB_Y
    if not verify(a['Y'], a['SigB_Y'], a['B'], a['g']):
        print("FUCKUP AT SigB_Y")
        return

    # Shared secret
    a['K'] = a['Y'] ** a['x']

    # Check MacK_B
    if a['MacK_B'] != MAC(a['B'], a['K']):
        print("FUCKUP AT MacK_B")
        return

    # Signatures
    a['SigA_X'] = sign(a['X'], a['a'])
    a['SigA_Y'] = sign(a['Y'], a['a'])

    # MAC
    a['MacK_A'] = MAC(a['A'], a['K'])

    return {
        'A': a['A'],
        'SigA_X': a['SigA_X'], 'SigA_Y': a['SigA_Y'], 'MacK_A': a['MacK_A']
    }


def step_3(b):
    # Check SigA_X
    if not verify(b['X'], b['SigA_X'], b['A'], b['g']):
        print("FUCKUP AT SigA_X")
        return

    # Check SigA_Y
    if not verify(b['Y'], b['SigA_Y'], b['A'], b['g']):
        print("FUCKUP AT SigA_Y")
        return

    if b['MacK_A'] != MAC(b['A'], b['K']):
        print("FUCKUP AT MacK_B")
        return

    return True

def main():
    # Just testing
    g = G.random(G1)

    a = {'g': g}
    b = {'g': g}

    b.update(step_0(a))
    a.update(step_1(b))
    b.update(step_2(a))
    print(step_3(b))

if __name__ == "__main__":
    main()
