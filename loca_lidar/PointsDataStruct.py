import numpy as np

CartesianPoints = np.dtype([
        ('x', np.float64),
        ('y', np.float64),
    ])

PolarPoints = np.dtype([
        ('distance', np.float64),
        ('angle', np.float64),
    ])

DistPts = np.dtype([
        ('pt1', np.int64),
        ('pt2', np.int64),
        ('squared_dist', np.float64),
    ])
