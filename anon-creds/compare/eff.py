from charm.toolbox.pairinggroup import PairingGroup, ZR, G1, G2, GT, pair
from utils import product
import time

G = PairingGroup('SS512')

## ------------- ISSUE -------------

def step_0(u):
    u['M'] = u['g'] ** u['m'][0] * product([Z ** m for Z, m in zip(u['Z'], u['m'][1:])])
    u['r'] = G.random(ZR, len(u['m']))
    u['T'] = u['g'] ** u['r'][0] * product([Z ** r for Z, r in zip(u['Z'], u['r'][1:])])
    return {'M': u['M'], 'T': u['T']}

def step_1(i):
    i['c'] = G.random(ZR)
    return {'c': i['c']}

def step_2(u):
    u['s'] = [r - u['c'] * m for r, m in zip(u['r'], u['m'])]
    return {'s': u['s']}

def step_3(i):
    lhs = i['T']
    rhs = i['M'] ** i['c'] * i['g'] ** i['s'][0] * product([Z ** s for Z, s in zip(i['Z'], i['s'][1:])])

    if lhs != rhs:
        raise ValueError("Step3 fuckup on check")

    a0 = G.random(ZR)
    i['A'] = [i['g'] ** a0]
    i['A'] += [i['A'][0] ** z for z in i['z']]
    i['B'] = [A ** i['y'] for A in i['A']]
    i['C'] = i['A'][0] ** i['x'] * i['M'] ** (a0 * i['x'] * i['y'])

    return {'A': i['A'], 'B': i['B'], 'C': i['C']}


## ------------- VERIFY -------------

def step_4(u):
    u["r"], u["r'"] = G.random(ZR, 2)
    u['At'] = [A ** u["r'"] for A in u['A']]
    u['Bt'] = [B ** u["r'"] for B in u['B']]
    u['Ct'] = u['C'] ** (u["r'"] * u["r"])

    u['kr'], *u['k'] = G.random(ZR, len(u['m']) + 3)

    prod = product([Bt ** k for Bt, k in zip(u['Bt'], u['k'])])
    u['T'] = u['At'][0] ** u['kr'] * prod
    #
    # prod = product([pair(u['X'], Bt) ** r for Bt, r in zip(u['Bt'], u['r'])])
    # u['td'] = pair(u['X'], u['At'][0]) ** u['ra'] * prod

    return {'At': u['At'], 'Bt': u['Bt'], 'Ct': u['Ct'], 'T': u['T']}

def step_5(v):
    v['c'] = G.random(ZR)
    return {'c': v['c']}

def step_6(u):
    u['sr'] = u['kr'] - u['c'] * u['r']

    # u['sa'] = u['ra'] - u['c'] * u["r''"]
    u['s'] = [k - u['c'] * m * u["r"] for k, m in zip(u['k'], u['m'])]
    return {'sr': u['sr'], 's': u['s']}

def step_7(v):
    """ Verifier - Verify """

    if not all([pair(Z, v['At'][0]) == pair(v['g'], At) for Z, At in zip(v['Z'], v['At'][1:])]):
        raise ValueError("Paring LHS != RHS")

    if not all([pair(v['Y'], At) == pair(v['g'], Bt)] for At, Bt in zip(v['At'], v['Bt'])):
        raise ValuseError("Pairing LHS != RHS")

    lhs = pair(v['g'], v['Ct'] ** v['c'])

    prod = product([Bt ** s for Bt, s in zip(v['Bt'], v['s'])])
    rhs = pair(v['X'], v['T'] / (v['At'][0] ** v['sr']) / prod)

    # prod = product([pair(v['X'], B) ** s for B, s in zip(v['Bt'], v['s'])])
    # rhs = pair(v['g'], v['Ct']) ** v['c'] * pair(v['X'], v['At'][0]) ** v['sa'] * prod
    accept = lhs == rhs
    return {"Accept": accept}


def test():
    # Just testing
    l = 10

    g = G.random(G1)
    x, y = G.random(ZR), G.random(ZR)
    z = [G.random(ZR) for _ in range(l)]
    m = [G.random(ZR) for _ in range(l+1)]

    X, Y = g ** x, g ** y
    Z = [g ** i for i in z]


    iters = 30
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
