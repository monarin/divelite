import compute_memview as compute_cy
import numpy as np
array_1 = np.random.uniform(0, 1000, size=(3000, 2000)).astype(np.intc)
array_2 = np.random.uniform(0, 1000, size=(3000, 2000)).astype(np.intc)
a = 4
b = 3
c = 9
compute_cy.compute(array_1, array_2, a, b, c)
