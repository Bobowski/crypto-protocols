#!/usr/bin/env python3

from charm.toolbox.pairinggroup import PairingGroup, ZR, G1, G2, GT, pair

from utils import b64encode, jencode

import json
import base64


if __name__ == "__main__":
    G = PairingGroup('SS512')

    l = int(input('l: '))
    g = input("g: ")
    g = G.random(G1) if g == "" else G.deserialize(base64.b64decode(g))
    # Secret
    x, y = G.random(ZR), G.random(ZR)
    z = G.random(ZR, count=l) if l > 1 else [G.random(ZR)]
    # Public
    X, Y = g ** x, g ** y
    Z = [g ** zi for zi in z]
    # messages
    m = G.random(ZR, l+1)

    v = {'g': g, 'X': X, 'Y': Y, 'Z': Z}
    i = {'g': g, 'x': x, 'y': y, 'z': z}
    i.update(v)
    u = {'m': m}

    print("Generated credentials: {}".format(json.dumps(b64encode(i), indent=4)))

    with open("cred.pk", "w+") as f:
        f.write(jencode(v))

    with open("cred.sk", "w+") as f:
        f.write(jencode(i))

    with open("msgs", "w+") as f:
        f.write(jencode(u))
