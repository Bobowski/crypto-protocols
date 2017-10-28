from functools import reduce

from charm.toolbox.pairinggroup import PairingGroup, ZR, G1, G2, GT, pair

G = PairingGroup('SS512')

def exp_prod(gs, ns):
    return reduce(lambda x, y: x * y, [g ** n for g, n in zip(gs, ns)])

# Issuing credentials
def step_0(u):
    u['M'] = u['g'] ** u['m'][0] * exp_prod(u['Z'], u['m'][1:])
    u['r'] = G.random(ZR, len(u['m']))
    u['T'] = u['g'] ** u['r'][0] * exp_prod(u['Z'], u['r'][1:])
    return {'M': u['M'], 'T': u['T']}

def step_1(i):
    i['c'], i['ω'] = G.random(ZR, 2)
    i['g̃'] = i['g'] ** i['ω']
    return {'c': i['c'], 'g̃': i['g̃']}

def step_2(u):
    u['S'] = [u['g̃'] ** (r - u['c'] * m) for r, m in zip(u['r'], u['m'])]
    return {'S': u['S']}

def step_3(i):
    lhs = pair(i['g̃'], i['T'] / (i['M'] ** i['c']))
    rhs = pair(i['S'][0], i['g']) * G.pair_prod(i['S'][1:], i['Z'])
    if lhs != rhs:
        raise ValueError("Paring LHS != RHS")

    # A
    a0 = G.random(ZR)
    i['A'] = [i['g'] ** a0]
    i['A'] += [i['A'][0] ** z for z in i['z']]
    # B
    i['B'] = [A ** i['y'] for A in i['A']]
    # C
    i['C'] = (i['A'][0] ** x) * (i['M'] ** (a0 * x * y))

    return {'A': i['A'], 'B': i['B'], 'C': i['C']}

def step_4(u):
    return {'m': u['m'], 'A': u['A'], 'B': u['B'], 'C': u['C']}


# Verifying credentials

def step_6(u):
    u["r'"], u["r''"], u['ra'], *u['r'] = G.random(ZR, len(u['m']) + 3)
    u['At'] = [A ** u["r'"] for A in u['A']]
    u['Bt'] = [B ** u["r'"] for B in u['B']]
    u['Ct'] = u['C'] ** (u["r'"] * u["r''"])

    prod = [pair(u['X'], Bt) ** r for Bt, r in zip(u['Bt'], u['r'])]
    prod = reduce(lambda x, y: x * y, prod)
    u['td'] = pair(u['X'], u['At'][0]) ** u['ra'] * prod

    return {'At': u['At'], 'Bt': u['Bt'], 'Ct': u['Ct'], 'td': u['td']}

def step_7(v):
    if not all([pair(v['At'][0], Z) == pair(v['g'], At) for Z, At in zip(u['Z'], u['At'][1:])]):
        raise ValueError("Paring LHS != RHS")

    if not all([pair(At, u['Y']) == pair(u['g'], Bt)] for At, Bt in zip(u['At'], u['Bt'])):
        raise ValuseError("Pairing LHS != RHS")

    v['c'], v['ω'] = G.random(ZR, 2)
    v['Xd'] = v['X'] ** v['ω']
    return {'c': v['c'], 'Xd': v['Xd']}

def step_8(u):
    u['sa'] = u['ra'] - u['c'] * u["r''"]
    u['S'] = [u['Xd'] ** (r - u['c'] * m * u["r''"]) for r, m in zip(u['r'], u['m'])]
    return {'sa': u['sa'], 'S': u['S']}

def step_9(v):
    lhs = v['td'] ** v['ω']
    rhs = pair(v['g'] ** (v['ω'] * v['c']), v['Ct']) * pair(v['Xd'], v['At'][0]) ** v['sa'] * G.pair_prod(u['S'], u['Bt'])

    accept = lhs == rhs
    return {"Accept": accept}


if __name__ == "__main__":
    # Just testing
    l = 5

    g = G.random(G1)
    x, y = G.random(ZR), G.random(ZR)
    z = [G.random(ZR) for _ in range(l)]
    m = [G.random(ZR) for _ in range(l+1)]

    X, Y = g ** x, g ** y
    Z = [g ** i for i in z]

    i = {'g': g, 'x': x, 'y': y, 'z': z}
    v = {'g': g, 'X': X, 'Y': Y, 'Z': Z}
    u = {'g': g, 'X': X, 'Y': Y, 'Z': Z, 'm': m}
    i.update(v)

    i.update(step_0(u))
    u.update(step_1(i))
    i.update(step_2(u))
    u.update(step_3(i))
    print(step_4(u))

    v.update(step_6(u))
    u.update(step_7(v))
    v.update(step_8(u))
    print(step_9(v))
