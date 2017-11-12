#!/usr/bin/env python3

from charm.toolbox.pairinggroup import PairingGroup, ZR, G1, G2, GT, pair

from schnorr import step_1 as verify
from utils import jencode, jdecode


if __name__ == "__main__":
    # Read {g, pk}
    v = jdecode(input("pub: "))
    v.update(jdecode(input("m: ")))
    v.update(jdecode(input("sign: ")))

    print(verify(v))
