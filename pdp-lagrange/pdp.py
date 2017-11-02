from functools import reduce

from charm.toolbox.integergroup import IntegerGroupQ, integer

from utils import Poly, product

import random
import hashlib


# Setup
G = IntegerGroupQ()
G.paramgen(1024)
g = G.randomG()
sk = G.random()
z = 16
n = 256
NUM_BLOCKS = 1

# Client message
M = [[integer(random.randrange(2 ** n), G.q) for _ in range(z)] for _ in range(NUM_BLOCKS)]


def block_id(f):
    """ Helper function to calculate ID(f) """
    return hashlib.sha1(str(f).encode('utf-8')).hexdigest()

def Lx(L, x):
    """ Calculate value of polynomial L in point x """
    return reduce(lambda acc, a: acc * x + a, L)

def LIexp(phi, xc):
    """ Calculate LIexp for elements phi in point xc """
    return product(
        grLx ** product((xc - mj) / (m - mj) for mj, _ in phi if mj != m)
        for m, grLx in phi
    )

def poly(sk, fid):
    """ Generate random polynomial from seed := sk + id_f """
    random.seed(str(sk) + fid)  # Seed initialized by string sk + fid
    return [integer(random.randrange(G.q), G.q) for _ in range(z + 1)]

def agg_poly(sk, fid, Mid):
    """ Aggregated polynomial generation - same az for all polynomials """
    p = poly(sk, fid)
    random.seed(str(sk) + Mid)
    p[-1] = integer(random.randrange(G.q), G.q)
    return p

def tag_block(sk, f):
    """ Calculate tags for block f """
    Lf = poly(sk, block_id(f))
    return [(m, Lx(Lf, m)) for m in f]

def gen_challange(sk, fid):
    """ Client - Generate challange for server """
    Lf = poly(sk, fid)
    r = G.random()
    xc = G.random()  # CAUTION: xc != mi

    Kf = g ** (r * Lx(Lf, xc))
    H = (g ** r, xc, g ** (r * Lx(Lf, integer(0, G.q))))
    return (Kf, H)

def pub_challange(PKf):
    """ Verifier - Public verification of posession """
    gr, xc, grLf0, grLfxc = PKf
    r = G.random()
    Kf = grLfxc ** r
    H = (gr ** r, xc, grLf0 ** r)
    return (Kf, H)

def agg_gen_challange(sk, F, Mid):
    """ Aggregated challange generation """
    Lfs = [agg_poly(sk, fid, Mid) for fid in F]
    r = G.random()
    xc = G.random()  # xc != m foreach m in f
    Kf = product(g ** Lx(Lf, xc) for Lf in Lfs)
    H = (g ** r, xc, g ** (r * Lfs[0][-1]))
    return (Kf, H)

def gen_proof(Tf, H):
    """ Server - Generate proof of posession """
    gr, xc, grLf0 = H
    phi = [(integer(0, G.q), grLf0)] + [(m, gr ** t) for m, t in Tf]
    Pf = LIexp(phi, xc)
    return Pf

def agg_gen_proof(Tfs, H):
    gr, xc, grLf0 = H
    return product(
        LIexp([(integer(0, G.q), grLf0)] + [(m, gr ** t) for m, t in Tf], xc)
        for Tf in Tfs
    )


t = tag_block(sk, M[0])
Kf, H = gen_challange(sk, block_id(M[0]))
Pf = gen_proof(t, H)

print(Pf == Kf)
