#!/usr/bin/env python3

from charm.toolbox.pairinggroup import PairingGroup, ZR, G1, G2, GT, pair

from anon_creds import step_6 as commit
from anon_creds import step_8 as answer

from utils import jencode, jdecode


if __name__ == "__main__":
    # Read {g, X, Y, Z, m}
    u = jdecode(input("crds: "))
    u.update(jdecode(input("pk: ")))

    # Commit
    print(jencode(commit(u)))

    # Await challange
    u.update(jdecode(input("c: ")))

    # Answer challange
    print(jencode(answer(u)))
