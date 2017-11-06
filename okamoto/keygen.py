#!/usr/bin/env python3

from charm.toolbox.pairinggroup import PairingGroup, ZR, G1, G2, GT, pair

from utils import b64encode, jencode, product

import json
import base64


if __name__ == "__main__":
    G = PairingGroup('SS512')

    # (g1, g2)
    g1 = input("g1: ")
    g1 = G.random(G1) if g1 == "" else G.deserialize(base64.b64decode(g1))
    g2 = input("g2: ")
    g2 = G.random(G1) if g2 == "" else G.deserialize(base64.b64decode(g2))
    g = (g1, g2)

    skey = G.random(ZR, 2)
    pkey = product(g_ ** a for g_, a in zip(g, skey))

    pk = {"g": g, "pk": pkey}
    sk = {"g": g, "pk": pkey, "sk": skey}

    print("Generated credentials: {}".format(json.dumps(b64encode(sk), indent=4)))

    with open("cred.pk", "w+") as f:
        f.write(jencode(pk))

    with open("cred.sk", "w+") as f:
        f.write(jencode(sk))
