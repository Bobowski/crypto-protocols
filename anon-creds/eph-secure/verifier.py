#!/usr/bin/env python3

from charm.toolbox.pairinggroup import PairingGroup, ZR, G1, G2, GT, pair

from anon_creds import step_7 as challange
from anon_creds import step_9 as verify

from utils import jencode, jdecode


if __name__ == "__main__":
    # Read {g, x, y, z, X, Y, Z}
    v = jdecode(input("pk: "))

    # Await commit
    v.update(jdecode(input("commit: ")))

    # Create challange
    print(jencode(challange(v)))

    # Await answer to challange
    v.update(jdecode(input("anwser: ")))

    # Issue credentials
    print(verify(v))
