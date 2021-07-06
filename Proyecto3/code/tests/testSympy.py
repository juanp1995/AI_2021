from numpy import random
from numpy.random import randint
from numpy.random import rand
import numpy as np
import sympy

k1, k2, x = sympy.symbols('k1 k2 x')

h = k1 * sympy.exp(k2*x) + k1 * sympy.sin(k2*x)
t = k1 + k1*sympy.cos(k2*x)

fh = sympy.lambdify((k1, k2, x), h, 'numpy')
ft = sympy.lambdify((k1, k2, x), t, 'numpy')

print(fh(2,2,1))



# test = list()

# l = randint(0, 5)
# print(l)

# out = [int(x) for x in '{:0{size}b}'.format(l,size=3)]
# print(out)

# bits = randint(0, 2, 32 * 4).tolist()
# out = out + bits
# print(out)