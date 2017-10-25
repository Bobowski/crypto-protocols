#!/usr/local/bin/python3

from charm.toolbox.pairinggroup import PairingGroup, ZR, G1, G2, GT, pair

from schnorr import step_0 as commit
from schnorr import step_2 as answer
from utils import jencode, jdecode


if __name__ == "__main__":
    # Read {g, sk [,pk]}
    p = jdecode(input("priv: "))

    # Commit X
    print(jencode(commit(p)))

    # Await challange x
    p.update(jdecode(input("c: ")))

    # Answer challange with p
    print(jencode(answer(p)))
