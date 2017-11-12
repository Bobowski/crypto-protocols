from functools import reduce

from charm.toolbox.pairinggroup import PairingGroup, ZR, G1, G2, GT, pair

import base64
import json

G = PairingGroup('SS512')


def product(A):
    return reduce(lambda x, y: x * y, A)


def b64encode(d):
    if isinstance(d, (list, tuple)):
        return [b64encode(a) for a in d]
    if isinstance(d, dict):
        return {k: b64encode(v) for k, v in d.items()}
    return base64.b64encode(G.serialize(d)).decode('UTF-8')

def b64decode(d):
    if isinstance(d, list):
        return [b64decode(a) for a in d]
    if isinstance(d, dict):
        return {k: b64decode(v) for k, v in d.items()}
    return G.deserialize(base64.b64decode(d))


def jencode(d):
    return json.dumps(b64encode(d))

def jdecode(d):
    return b64decode(json.loads(d))
