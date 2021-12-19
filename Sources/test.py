import numpy as np
import math
from scipy.optimize import linear_sum_assignment
import pygame
cost=np.array([[np.inf,2,np.inf],[5,np.inf,2],[np.inf,4,np.inf]])
row_ind, col_ind = linear_sum_assignment(cost)
print(row_ind)
print(col_ind)
print(cost[row_ind,col_ind].sum())
print(pygame.font.get_fonts())

a = np.str_('$3')
print(type(a))
print(a in '$33')