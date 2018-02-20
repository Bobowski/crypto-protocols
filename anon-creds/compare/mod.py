from charm.toolbox.pairinggroup import PairingGroup, ZR, G1, G2, GT, pair
from utils import product
import time

G = PairingGroup('SS512')

# Issuing credentials
def step_0(u):
    """ User - Commit """
    u['M'] = u['g'] ** u['m'][0] * product([Z ** m for Z, m in zip(u['Z'], u['m'][1:])])
    u['r'] = G.random(ZR, len(u['m']))
    u['T'] = u['g'] ** u['r'][0] * product([Z ** r for Z, r in zip(u['Z'], u['r'][1:])])
    return {'M': u['M'], 'T': u['T']}

def step_1(i):
    """ Issuer - Challange """
    i['c'], i['ω'] = G.random(ZR, 2)
    i['g̃'] = i['g'] ** i['ω']
    return {'c': i['c'], 'g̃': i['g̃']}

def step_2(u):
    """ User - Answer challange """
    u['S'] = [u['g̃'] ** (r - u['c'] * m) for r, m in zip(u['r'], u['m'])]
    return {'S': u['S']}

def step_3(i):
    """ Issuer - Issue credentials """
    lhs = pair(i['g̃'], i['T'] / (i['M'] ** i['c']))
    # rhs = pair(i['S'][0], i['g']) * G.pair_prod(i['S'][1:], i['Z'])
    rhs = pair(i['S'][0], i['g']) * product([pair(S, Z) for S, Z in zip(i['S'][1:], i['Z'])])
    if lhs != rhs:
        raise ValueError("Paring LHS != RHS")

    # A
    a0 = G.random(ZR)
    i['A'] = [i['g'] ** a0]
    i['A'] += [i['A'][0] ** z for z in i['z']]
    # B
    i['B'] = [A ** i['y'] for A in i['A']]
    # C
    i['C'] = (i['A'][0] ** i['x']) * (i['M'] ** (a0 * i['x'] * i['y']))

    return {'A': i['A'], 'B': i['B'], 'C': i['C']}


# Verifying credentials
def step_4(u):
    """ User - Commit """
    u["r'"], u["r''"], u['ra'], *u['r'] = G.random(ZR, len(u['m']) + 3)
    u['At'] = [A ** u["r'"] for A in u['A']]
    u['Bt'] = [B ** u["r'"] for B in u['B']]
    u['Ct'] = u['C'] ** (u["r'"] * u["r''"])

    prod = product([pair(u['X'], Bt) ** r for Bt, r in zip(u['Bt'], u['r'])])
    u['td'] = pair(u['X'], u['At'][0]) ** u['ra'] * prod

    return {'At': u['At'], 'Bt': u['Bt'], 'Ct': u['Ct'], 'td': u['td']}

def step_5(v):
    """ Verifier - Challange """
    if not all([pair(v['At'][0], Z) == pair(v['g'], At) for Z, At in zip(v['Z'], v['At'][1:])]):
        raise ValueError("Paring LHS != RHS")

    if not all([pair(At, v['Y']) == pair(v['g'], Bt)] for At, Bt in zip(v['At'], v['Bt'])):
        raise ValuseError("Pairing LHS != RHS")

    v['c'], v['ω'] = G.random(ZR, 2)
    v['Xd'] = v['X'] ** v['ω']
    return {'c': v['c'], 'Xd': v['Xd']}

def step_6(u):
    """ User - Answer challange """
    u['sa'] = u['ra'] - u['c'] * u["r''"]
    u['S'] = [u['Xd'] ** (r - u['c'] * m * u["r''"]) for r, m in zip(u['r'], u['m'])]
    return {'sa': u['sa'], 'S': u['S']}

def step_7(v):
    """ Verifier - Verify """
    lhs = v['td'] ** v['ω']
    prod = product([pair(S, B) for S, B in zip(v['S'], v['Bt'])])

    rhs = pair(v['g'] ** (v['ω'] * v['c']), v['Ct']) * pair(v['Xd'], v['At'][0]) ** v['sa'] * prod

    accept = lhs == rhs
    return {"Accept": accept}


def test():
    # Just testing
    l = 1999

    g = G.random(G1)
    x, y = G.random(ZR), G.random(ZR)
    z = [G.random(ZR) for _ in range(l)]
    m = [G.random(ZR) for _ in range(l+1)]

    X, Y = g ** x, g ** y
    Z = [g ** i for i in z]


    iters = 2
    dta = []
    for _ in range(iters):
        u = {'g': g, 'X': X, 'Y': Y, 'Z': Z, 'm': m}
        i = {'g': g, 'x': x, 'y': y, 'z': z}
        v = {'g': g, 'X': X, 'Y': Y, 'Z': Z}
        i.update(v)

        dta.append((u, i, v))

    ## ---------- TIME TESTING ---------
    issue_t = time.time()
    for u, i, v in dta:
        i.update(step_0(u))
        u.update(step_1(i))
        i.update(step_2(u))
        u.update(step_3(i))

    issue_t = time.time() - issue_t

    verify_t = time.time()
    for u, i, v in dta:
        v.update(step_4(u))
        u.update(step_5(v))
        v.update(step_6(u))
        step_7(v)

    verify_t = time.time() - verify_t

    ## ---------- TIME TESTING ---------

    print("msg:", l + 1)
    print("issue:", issue_t, "avg:", issue_t / iters)
    print("verify:", verify_t, "avg:", verify_t / iters)
    print("total:", issue_t + verify_t, "avg:", (issue_t + verify_t)/iters)

if __name__ == "__main__":
    test()
