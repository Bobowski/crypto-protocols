from charm.toolbox.pairinggroup import PairingGroup, ZR, G1, G2, GT, pair

import base64
import json

G = PairingGroup('SS512')


def b64encode(d):
    return {
        k: base64.b64encode(G.serialize(v)).decode('UTF-8')
        for k, v in d.items()
    }

def b64decode(d):
    return {
        k: G.deserialize(base64.b64decode(v))
        for k, v in d.items()
    }

def jencode(d):
    return json.dumps(b64encode(d))

def jdecode(d):
    return b64decode(json.loads(d))
