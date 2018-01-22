import time

from charm.toolbox.ecgroup import ECGroup
from charm.toolbox.eccurve import prime192v1, prime256v1
from charm.toolbox.pairinggroup import PairingGroup, ZR, G1, G2, GT

from rom import OkamotoRom
from standard import OkamotoStd
from ephemeral import OkamotoEph


tests = {
    "SS512": (PairingGroup('SS512'), [OkamotoRom, OkamotoEph, OkamotoStd]),
    "MNT224": (PairingGroup('MNT224'), [OkamotoRom, OkamotoEph, OkamotoStd]),
    "prime192v1": (ECGroup(prime192v1), [OkamotoEph, OkamotoStd]),
    "prime256v1": (ECGroup(prime256v1), [OkamotoEph, OkamotoStd])
}

for curve, suit in tests.items():
    print(curve)



    G, IDSs = suit
    if curve == "MNT224":
        g = [G.random(G2) for _ in range(2)]
    else:
        g = [G.random(G1) for _ in range(2)]
               
    sk = [G.random(ZR) for _ in range(2)]
    pk = g[0] ** sk[0] * g[1] ** sk[1]

    pm = {'sk': sk, 'g': g}
    vm = {'pk': pk, 'g': g}

    for IDS_cls in IDSs:
        IDS = IDS_cls(G)

        p = dict(pm)
        v = dict(vm)

        start = time.time()

        for i in range(100):
            v.update(IDS.commit(p))
            p.update(IDS.challenge(v))
            v.update(IDS.answer(p))
            res = IDS.verify(v)

        duration = time.time() - start

        if not res:
            raise ValueError("Invalid identification")

        print(IDS.__class__.__name__, res, duration)
