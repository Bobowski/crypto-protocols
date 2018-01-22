import random
import os

from charm.toolbox.symcrypto import SymmetricCryptoAbstraction,AuthenticatedCryptoAbstraction, MessageAuthenticator

from charm.toolbox.pairinggroup import PairingGroup, ZR, G1, G2, GT, pair
from charm.core.math.pairing import hashPair as sha2

G = PairingGroup('SS512')

def enc(k1, k2, msg):
    a1 = SymmetricCryptoAbstraction(k1)
    a2 = SymmetricCryptoAbstraction(k2)
    c0 = a1.encrypt(msg)
    c1 = a2.encrypt(c0)
    return c1

def dec(k1, k2, ct):
    a1 = SymmetricCryptoAbstraction(k1)
    a2 = SymmetricCryptoAbstraction(k2)
    m0 = a2.decrypt(ct)
    m1 = a1.decrypt(m0)
    return m1

A_0, A_1 = [os.urandom(128) for _ in range(2)]
B_0, B_1 = [os.urandom(128) for _ in range(2)]
C_0, C_1 = [os.urandom(128) for _ in range(2)]

Table = [
    enc(A_0, B_0, C_0),
    enc(A_0, B_1, C_0),
    enc(A_1, B_0, C_0),
    enc(A_1, B_1, C_1)
]
# random.shuffle(Table)


Alice_A = A_1
Bob_b   = B_1

for i, t in enumerate(Table):
    try:
        a = dec(Alice_A, Bob_b, t)
        print(a == C_1)
        print(a == C_0)
    except:
        pass
