#!/usr/bin/env python3

from charm.toolbox.pairinggroup import PairingGroup, ZR, G1, G2, GT, pair

from anon_creds import step_1 as challange
from anon_creds import step_3 as issue

from utils import jencode, jdecode


if __name__ == "__main__":
    # Read {g, x, y, z, X, Y, Z}
    i = jdecode(input("sk: "))

    # Await commit
    i.update(jdecode(input("commit: ")))

    # Create challange
    print(jencode(challange(i)))

    # Await answer to challange
    i.update(jdecode(input("anwser: ")))

    # Issue credentials
    print(jencode(issue(i)))
