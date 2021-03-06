import numpy as np
import patsy

class Transform:
    """ Transformation class

    All children of Transform must have transfom and untransform methods
    """
    pass


class ZTransform(Transform):
    """
    """
    def __init__(self, x):
        self._mean = np.nanmean(x, axis=0)
        self._std = np.nanstd(x, axis=0)
    
    def transform(self, x):
        return (x - self._mean)/self._std

    def untransform(self, x):
        return x*self._std + self._mean

class UnitTransform(Transform):
    def __init__(self, x):
        self._max = np.nanmax(x, axis=0)
    
    def transform(self, x):
        return x/self._max

    def untransform(self, x):
        return x*self._max

class LogZTransform(ZTransform):
    """
    Handle negative values
    """
    def __init__(self, x):

        log_x = np.log(x)
        super().__init__(log_x)

    def transform(self, x):
        log_x = np.log(x)
        return super().transform(log_x)
        

    def untransform(self, z=None):
        #if x is None:
        #    return self._x

        #else:
        log_x = super().untransform(z)
        return np.exp(log_x)
    
    
class Dmatrix(Transform):
    def __init__(self, knots, degree, form):
        self.form = f"{form}(stage, knots=knots, degree={degree}, include_intercept=True) - 1"
        self.knots = knots
    
    def transform(self, stage):
        return patsy.dmatrix(self.form, {"stage": stage, "knots": self.knots[1:-1]})