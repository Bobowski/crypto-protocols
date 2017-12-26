from charm.toolbox.integergroup import IntegerGroupQ, integer

from utils import ID, Poly, product, LIexp

import random

import time

# Setup
G = IntegerGroupQ()
G.paramgen(1024)
g = G.randomG()
sk = G.random()
z = 16
n = 256
NUM_BLOCKS = 1

print("Params")

# Client message
M = [[integer(random.randrange(2 ** n), G.q) for _ in range(z)] for _ in range(NUM_BLOCKS)]

print("File")

def poly(sk, fid):
    """ Generate random polynomial from seed := sk + id_f """
    random.seed(str(sk) + fid)  # Seed initialized by string sk + fid
    return Poly([integer(random.randrange(G.q), G.q) for _ in range(z + 1)])

def agg_poly(sk, fid, Mid):
    """ Aggregated polynomial generation - same a0 for all polynomials """
    p = poly(sk, fid)
    random.seed(str(sk) + Mid)
    p[0] = integer(random.randrange(G.q), G.q)
    return p

def tag_block(sk, f):
    """ Calculate tags for block f """
    Lf = poly(sk, ID(f))
    return [(m, Lf(m)) for m in f]

def agg_tag_block(sk, f, Mid):
    Lf = agg_poly(sk, ID(f), Mid)
    return [(m, Lf(m)) for m in f]

def gen_challange(sk, fid):
    """ Client - Generate challange for server """
    Lf = poly(sk, fid)
    r = G.random()
    xc = G.random()  # CAUTION: xc != mi

    Kf = g ** (r * Lf(xc))
    H = (g ** r, xc, g ** (r * Lf[0]))
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
    Lf, *_ = Lfs
    Kf = product(g ** (r * Lf(xc)) for Lf in Lfs)
    H = (g ** r, xc, g ** (r * Lf[0]))
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

a = time.time()

t = tag_block(sk, M[0])
Kf, H = gen_challange(sk, ID(M[0]))
Pf = gen_proof(t, H)

print(time.time() - a)
print(Pf == Kf)

a = time.time()

Tfs = [agg_tag_block(sk, f, ID(M)) for f in M]
Kf, H = agg_gen_challange(sk, [ID(f) for f in M], ID(M))
Pf = agg_gen_proof(Tfs, H)

print(time.time() - a)
print(Pf == Kf)
