import random

from charm.toolbox.integergroup import IntegerGroupQ, integer
from charm.core.math.integer import reduce as reduce_int

from utils import Poly, product, LI

G = IntegerGroupQ()
G.paramgen(512)

k = 4
m = 4
dp = 12
alpha = G.random()
P = Poly([G.random() for _ in range(dp+1)])

# Sender hides P in bivariate polynomial
Px = Poly([G.random() for _ in range(dp * k +1)])
Px[0] = integer(0, G.q)

def Q(x, y):
    return reduce_int(Px(x) + P(y))

# The receiver hides alpha in a univariate polynomial

S = Poly([G.random() for _ in range(k + 1)])
S[0] = alpha

n = dp * k + 1
N = n * m

X = [G.random() for _ in range(N)]

# Choose random indices
T = list(range(N))
random.shuffle(T)
T = T[:n]

Y = [(x, S(x) if i in T else G.random()) for i, x in enumerate(X)]

# Evaluate
Qs = [(x, Q(x, y)) for x, y in Y]

A = [xq for i, xq in enumerate(Qs) if i in T]

a = LI(A, integer(0, G.q))
b = P(alpha)
print(a)
print(b)
print(a == b)
