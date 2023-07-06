import numpy as np

a = np.ones((4,4))
b = a.copy()
b[0, 2] = 4
b[:,1] = 3
print(a)