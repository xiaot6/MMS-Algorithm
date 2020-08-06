import numpy as np
import numpy.linalg as la

a = 3* (np.exp(2*0.96) - np.exp(2*0.9))

a = a/0.06
b = 6*np.exp(1.8)

print((a- b)/b)
