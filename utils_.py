import numpy as np

def mc_normalization(mc):

    for i in range(mc.shape[0]):
        total = np.sum(mc[i, ])
        if total == 0:
            mc[i, ] = [1.0 / mc.shape[1]]
        elif total > 0:
            mc[i, ] = mc[i, ] / total
        else:
            raise ValueError('Sum must be greater than or equal to zero !')
