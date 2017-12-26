import random

from charm.toolbox.pairinggroup import PairingGroup, ZR, G1, G2, GT, pair

from utils import product

G = PairingGroup('SS512')


AnB = G.random(ZR, 4)
A = G.random(ZR, 4) + AnB
B = G.random(ZR, 4) + AnB

print("done")

def step_0(a):
    a['e'] = G.random(ZR)
    a['g^e'] = [G.hash(m, G1) ** a['e'] for m in a['m']]

    return {"g^e": a['g^e']}

def step_1(b):
    b['f'] = G.random(ZR)
    b['g^f'] = [G.hash(m, G1) ** b['f'] for m in b['m']]
    b['g^ef'] = [ge ** b['f'] for ge in b['g^e']]

    return {"g^f": b['g^f'], "g^ef": b['g^ef']}

def step_2(a):
    a['g^fe'] = [gf ** a['e'] for gf in a['g^f']]

    common = [x for x in a['g^ef'] if x in a['g^fe']]
    print(len(common))

if __name__ == '__main__':
    a = {"m": A}
    b = {"m": B}

    b.update(step_0(a))
    a.update(step_1(b))
    step_2(a)
