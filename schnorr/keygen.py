#!/usr/bin/env python3

from charm.toolbox.pairinggroup import PairingGroup, ZR, G1, G2, GT, pair

from utils import b64encode, jencode

import json
import base64


if __name__ == "__main__":
    G = PairingGroup('SS512')

    g = input("g: ")
    g = G.random(G1) if g == "" else G.deserialize(base64.b64decode(g))
    skey = G.random(ZR)
    pkey = g ** skey

    pk = {"g": g, "pk": pkey}
    sk = {"g": g, "pk": pkey, "sk": skey}

    print("Generated credentials: {}".format(json.dumps(b64encode(sk), indent=4)))

    with open("cred.pk", "w+") as f:
        f.write(jencode(pk))

    with open("cred.sk", "w+") as f:
        f.write(jencode(sk))
