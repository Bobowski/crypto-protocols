#!/usr/bin/env python3

from charm.toolbox.pairinggroup import PairingGroup, ZR, G1, G2, GT, pair

from schnorr import step_1 as challange
from schnorr import step_3 as verify
from utils import jencode, jdecode


if __name__ == "__main__":
    # Read {g, pk}
    v = jdecode(input("pub: "))

    # Await commitment
    v.update(jdecode(input("X: ")))

    # Challange
    print(jencode(challange(v)))

    # Await response
    v.update(jdecode(input("s: ")))

    # Answer challange with p
    print(verify(v))
