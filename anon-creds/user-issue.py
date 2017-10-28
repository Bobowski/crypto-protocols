#!/usr/bin/env python3

from charm.toolbox.pairinggroup import PairingGroup, ZR, G1, G2, GT, pair

from anon_creds import step_0 as commit
from anon_creds import step_2 as answer
from anon_creds import step_4 as store

from utils import jencode, jdecode


if __name__ == "__main__":
    # Read {g, X, Y, Z, m}
    u = jdecode(input("pk: "))
    u.update(jdecode(input("m: ")))

    # Commit
    print(jencode(commit(u)))

    # Await challange
    u.update(jdecode(input("c: ")))

    # Answer challange
    print(jencode(answer(u)))

    # Await credentials
    u.update(jdecode(input("store: ")))

    # Store credentials
    print(jencode(store(u)))
