import time
import random

from charm.toolbox.ecgroup import ECGroup
from charm.toolbox.eccurve import prime192v1, prime256v1

from dh_simple import DHSimple
from dlp import DLP
from rsa import RSA
from pinkas import Pinkas

curve = prime192v1
key_size = 1024
M = 1
N = 1

print("Creating worlds...")
schemes = [DHSimple(ECGroup(curve)), DLP(ECGroup(curve)), Pinkas(ECGroup(curve)), RSA(key_size)]
Ms = [random.randrange(N) for _ in range(M)]


print("Testing OT", M, "of", N)
for OT in schemes:
    print(OT.__class__.__name__)
    a, b = OT.gen_params()
    OT.gen_msgs(a, N)

    ts_setup = time.time()
    b.update(OT.setup(a))
    ts_setup = time.time() - ts_setup

    ts_mask = []
    ts_total = time.time()
    for choice in Ms:
        b['b'] = choice

        a.update(OT.choose(b))

        ts_mask1 = time.time()
        b.update(OT.mask(a))
        ts_mask1 = time.time() - ts_mask1
        ts_mask.append((choice, ts_mask1))

        assert b["m"] == a["m'"][b["b"]]

    ts_total = time.time() - ts_total

    avg = 0
    for a in ts_mask:
        avg += a[1]
    avg /= len(ts_mask)
    print(OT.__class__.__name__, "Setup: ", ts_setup, " avg mask: ", avg, " all masks: ", ts_total, " total: ", ts_setup + ts_total)
