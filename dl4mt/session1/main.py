__author__ = 'HyNguyen'

import numpy as np

def testsoftmax():
    np.random.RandomState(4488)

    probs = np.random.rand(6,4)
    sum_probs = np.sum(probs,axis=1).reshape(6,1)
    probs /=sum_probs
    print probs

    y_flat = np.array ([1,2,3,0,2,1])
    y_flat_idx = np.arange(y_flat.shape[0]) * 4 + y_flat
    print(y_flat_idx)

    print '1', (probs[range(probs.shape[0]),y_flat])

    print "2", probs.flatten()[y_flat_idx]

if __name__ == "__main__":
    testsoftmax()