#!/usr/bin/env python3

from charm.core.math.integer import integer, random, randomPrime
from charm.schemes.pkenc.pkenc_rsa import RSA_Enc

from utils import b64encode, jencode

import json
import base64


if __name__ == "__main__":
    pk, sk = RSA_Enc().keygen(512)
    size = int(input("size: "))
    m = [random(pk['N']) for _ in range(size)]
    mg = {"m": m}

    print("Generated credentials: {}".format(json.dumps(b64encode(sk), indent=4)))

    with open("cred.pk", "w+") as f:
        f.write(jencode(pk))

    with open("cred.sk", "w+") as f:
        f.write(jencode(sk))

    with open("msg.mg", "w+") as f:
        f.write(jencode(mg))
