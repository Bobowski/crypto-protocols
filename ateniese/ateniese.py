import random as rnd
import hashlib

from charm.core.math.integer import integer,isPrime,gcd,random,randomPrime,toInt, serialize, deserialize


k = 160
l_p = 256
eps = 2
lambda_2 = 4 * l_p + 1
lambda_1 = eps * (lambda_2 + k) + 2 + 1
gamma_2 = lambda_1 + 2 + 1
gamma_1 = eps * (gamma_2 + k) + 2 + 1

A = (integer(2 ** lambda_1 - 2 ** lambda_2), integer(2 ** lambda_1 + 2 ** lambda_2))
T = (integer(2 ** gamma_1 - 2 ** gamma_2), integer(2 ** gamma_1 + 2 ** gamma_2))


def is_cyclic(a, n):
    one = integer(1, n)
    return gcd(a + one, n) == 1 or gcd(a - one, n) == 1


def setup():
    print("SETUP:")
    print("1. Select random l_p-bit primes and modulus n = pq")
    while True:
        p, q = randomPrime(l_p), randomPrime(l_p)
        if isPrime(p) and isPrime(q) and p != q:
            n = p * q
            phi_n = (p - 1) * (q - 1)
            break

    print("2. Choose random a, a_0, g, h in QR(n)")
    while True:
        g = random(n)
        if is_cyclic(g, n):
            g = g ** 2
            break
    a, a_0, h = [(g ** random(n)) % n for _ in range(3)]

    print("3. Choose random secret element x and set public key y = g**x")
    x = random(phi_n)
    y = (g ** x) % n

    print("4. The group public key Y: (n, a, a_0, y, g, h)")
    Y = {"n": n, "a": a, "a_0": a_0, "y": y, "g": g, "h": h}

    print("5. Corresponding secret key S: (p, q, phi_n, x)")
    S = {"p": p, "q": q, "phi_n": phi_n, "x": x}
    return (Y, S)


def join_0(u):
    print("JOIN:")
    print("1. User generates x and r and sends C_1 with proof")
    u["x"] = random(u["n"] ** 2)
    u["r"] = random(2 ** (2 * l_p))

    u["C_1"] = (u['g'] ** u['x'] * u['h'] ** u['r']) % u['n']

    return {"C_1": u["C_1"]}

def join_1(gm):
    print("2. GM checks C1 and selects alpha and beta")
    if not is_cyclic(gm["C_1"], gm['n']):
        print("ERROR!")
        return

    gm['alpha'], gm['beta'] = random(2 ** lambda_2), random(2 ** lambda_2)

    return {'alpha': gm['alpha'], 'beta': gm['beta']}

def join_2(u):
    print("3. User computes x_i and sends C_2 to GM")
    xa = (integer(u['alpha']) * integer(u['x']) + integer(u['beta'])) % (2 ** lambda_2)
    u['x'] = integer(2) ** lambda_1 + integer(xa)
    u['C_2'] = (u['a'] ** u['x']) % u['n']

    return {'C_2': u['C_2']}

def join_3(gm):
    print("4. GM checks C2 and computes random e_i prime")
    if not is_cyclic(gm['C_2'], gm['n']):
        print("ERROR")
        return

    while True:
        e = integer(rnd.randrange(T[0], T[1]))
        if not isPrime(e):
            continue

        d = (e % gm['phi_n']) ** -1
        A = ((gm['C_2'] * gm['a_0']) ** d) % gm['n']
        break

    gm['e'] = e
    gm['A'] = A

    return {'A': A, 'e': e}

def join_4(u):
    print("5. User verifies credentials")

    lhs = integer(u['a'], u['n']) ** u['x'] * u['a_0']
    rhs = (u['A'] ** u['e']) % u['n']
    print(u['A'])
    print(lhs == rhs)


def sign(u, m):
    print("SIGN:")
    print("1. Generate random value w")
    w = random(2 ** l_p)
    T_1 = (u['A'] * u['y'] ** w) % u['n']
    T_2 = (u['g'] ** w) % u['n']
    T_3 = ((u['g'] ** u['e']) * (u['h'] ** w)) % u['n']

    print("2. Randomly choose r_1, r_2, r_3, and r_4")
    r_1 = random(2 ** (eps * (gamma_2 + k)))
    r_2 = random(2 ** (eps * (lambda_2 + k)))
    r_3 = random(2 ** (eps * (gamma_1 + 2 * l_p + k + 1)))
    r_4 = random(2 ** (eps * (2 * l_p + k)))

    print("(a) d_1, d_2, d_3, d_4")
    d_1 = ((T_1 ** r_1) / ((u['a'] ** r_2) * (u['y'] ** r_3))) % u['n']
    d_2 = ((T_2 ** r_1) / (u['g'] ** r_3)) % u['n']
    d_3 = (u['g'] ** r_4) % u['n']
    d_4 = ((u['g'] ** r_1) * (u['h'] ** r_4)) % u['n']

    print("(b) c = HASH()")
    c = integer(int(hashlib.sha1(
        serialize(u['g']) +
        serialize(u['h']) +
        serialize(u['y']) +
        serialize(u['a_0']) +
        serialize(u['a']) +
        serialize(T_1) +
        serialize(T_2) +
        serialize(T_3) +
        serialize(d_1) +
        serialize(d_2) +
        serialize(d_3) +
        serialize(d_4) +
        m.encode()
    ).hexdigest(), 16))
    print(c)

    print("(c) s_1, s_2, s_3, s_4")
    s_1 = integer(r_1) - c * (integer(u['e']) - 2 ** gamma_1)
    s_2 = integer(r_2) - c * (integer(u['x']) - 2 ** lambda_1)
    s_3 = integer(r_3) - c * integer(u['e']) * integer(w)
    s_4 = integer(r_4) - c * integer(w)

    print("3. Output signature")
    return {"c": c, "s_1": s_1, "s_2": s_2, "s_3": s_3, "s_4": s_4, "T_1": T_1, "T_2": T_2, "T_3": T_3}


def verify(u, m, s):
    print("VERIFY:")
    print("1. Compute c'")
    d_1_1 = (u['a_0'] ** s['c']) * s['T_1'] ** (s['s_1'] - s['c'] * (2 ** gamma_1))
    d_1_2 = (u['a'] ** (s['s_2'] - s['c'] * (2 ** lambda_1))) * u['y'] ** s['s_3']
    d_1 = (d_1_1 / d_1_2) % u['n']

    d_2 = ((s['T_2'] ** (s['s_1'] - s['c'] * (2 ** gamma_1))) / u['g'] ** s['s_3']) % u['n']

    d_3 = (s['T_2'] ** s['c'] * u['g'] ** s['s_4']) % u['n']

    d_4 = (s['T_3'] ** s['c'] * u['g'] ** (s['s_1'] - s['c'] * (2 ** gamma_1)) * u['h'] ** s['s_4']) % u['n']

    c = integer(int(hashlib.sha1(
        serialize(u['g']) +
        serialize(u['h']) +
        serialize(u['y']) +
        serialize(u['a_0']) +
        serialize(u['a']) +
        serialize(s['T_1']) +
        serialize(s['T_2']) +
        serialize(s['T_3']) +
        serialize(d_1) +
        serialize(d_2) +
        serialize(d_3) +
        serialize(d_4) +
        m.encode()
    ).hexdigest(), 16))

    print("2. Accept if and only if c = c'")
    if c == s['c']:
        print("ACCEPT")
        return True
    else:
        print("NOT ACCEPTED")
        return False


def open(gm, m, s):
    print("OPEN:")
    print("1. Check the signature via VERIFY")
    if not verify(gm, m, s):
        print("NOT VALIDATED")

    A = (s['T_1'] / s['T_2'] ** gm['x']) % gm['n']
    print(A)



def test_join():
    Y, S = setup()

    u = dict(Y)
    gm = dict(Y)
    gm.update(S)

    gm.update(join_0(u))
    u.update(join_1(gm))
    gm.update(join_2(u))
    u.update(join_3(gm))
    join_4(u)

def test_sign():
    Y, S = setup()

    u = dict(Y)
    gm = dict(Y)
    gm.update(S)

    gm.update(join_0(u))
    u.update(join_1(gm))
    gm.update(join_2(u))
    u.update(join_3(gm))
    join_4(u)

    s = sign(u, "Awsome message")
    verify(u, "Awsome message", s)

    open(gm, "Awsome message", s)


def main():
    # test_join()
    test_sign()

if __name__ == "__main__":
    main()
