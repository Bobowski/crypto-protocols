from functools import reduce

from charm.core.math.integer import integer,isPrime,gcd,random,randomPrime,toInt, serialize, deserialize

import base64
import json


def product(A):
    return reduce(lambda x, y: x * y, A)

#
# def b64encode(d):
#     if isinstance(d, (list, tuple)):
#         return [b64encode(a) for a in d]
#     if isinstance(d, dict):
#         return {k: b64encode(v) for k, v in d.items()}
#     return int(d)
#     # return base64.b64encode(serialize(d)).decode('UTF-8')
#
# def b64decode(d):
#     if isinstance(d, list):
#         return [b64decode(a) for a in d]
#     if isinstance(d, dict):
#         return {k: b64decode(v) for k, v in d.items()}
#     return integer(d)
#     # return deserialize(base64.b64decode(d))
#


def b64encode(d):
    if isinstance(d, (list, tuple)):
        return [b64encode(a) for a in d]
    if isinstance(d, dict):
        return {k: b64encode(v) if k not in ["cmd", "status", "msg", "name"] else v for k, v in d.items() }
    return base64.b64encode(serialize(d)).decode('UTF-8')

def b64decode(d):
    if isinstance(d, list):
        return [b64decode(a) for a in d]
    if isinstance(d, dict):
        return {k: b64decode(v) if k not in ["cmd", "status", "msg", "name",] else v for k, v in d.items()}
    return deserialize(base64.b64decode(d))


def jencode(d):
    return json.dumps(b64encode(d))

def jdecode(d):
    return b64decode(json.loads(d))
