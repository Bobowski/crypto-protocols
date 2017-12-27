#!/usr/bin/env python3

from charm.toolbox.pairinggroup import PairingGroup, ZR, G1, G2, GT, pair

from schnorr import step_0 as sign
from utils import jencode, jdecode


if __name__ == "__main__":
    # Read {g, sk [,pk]}
    s = jdecode(input("priv: "))
    s.update(jdecode(input("m: ")))

    # Sign message m
    print(jencode(sign(s)))
