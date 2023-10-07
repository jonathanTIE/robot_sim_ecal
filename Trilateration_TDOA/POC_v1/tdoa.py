import numpy as np
import scipy.optimize as opt
import time

SOUND_SPEED = 343.2 # m/s

#SOURCE : https://lo.calho.st/posts/tdoa-multilateration/
#TODO : jacobian shit
def sqrt_safe(a, b, c, d, Z):
    temp = 0
    out = np.power(a - b, 2.) + np.power(c - d, 2.) + Z
    temp = np.sqrt(out)
    if np.isnan(temp):
        return 0
    return temp

def functions(x0, y0, x1, y1, x2, y2, d01, d02, d12, Z):
    """ Given observers at (x0, y0), (x1, y1), (x2, y2) and TDOA between observers d01, d02, d12, this closure
        returns a function that evaluates the system of three hyperbolae for given event x, y.
    """
    def fn(args):
        x, y = args
        a = sqrt_safe(x,x1, y,y1, Z) - sqrt_safe(x, x0, y, y0, Z) - d01
        b = sqrt_safe(x,x2, y,y2, Z) - sqrt_safe(x, x0, y, y0, Z) - d02
        c = sqrt_safe(x,x2, y,y2, Z) - sqrt_safe(x, x1, y, y1, Z) - d12
        return [a, b, c]
    return fn

def find_position(tdoas):
    Z = 0.25

    x0, y0 = 0.0, 0.0
    x1, y1 = 1.50, 2.0
    x2, y2 = 3.00, 0.0

    xp, yp = 1.51, 1.5
    F = functions(x0, y0, x1, y1, x2, y2, (tdoas[0]) * SOUND_SPEED, (tdoas[1]) * SOUND_SPEED, (tdoas[2]) * SOUND_SPEED, Z)
    x, y = opt.leastsq(
        F, 
        x0=[xp, yp])
    return (x,y)

if __name__ == "__main__":
    x0, y0 = 0.0, 0.0
    x1, y1 = 1.50, 2.0
    x2, y2 = 3.00, 0.0

    distance1 = 2.34
    distance2 = 1.04
    distance3 = 1.68

    t0 = distance1 / SOUND_SPEED
    t1 = distance2 / SOUND_SPEED
    t2 = distance3 / SOUND_SPEED

    Z = 0.25 #(z-zbeacon)²

    t = time.time()
    xp, yp = 1.51, 1.5
    F = functions(x0, y0, x1, y1, x2, y2, (t1 - t0) * SOUND_SPEED, (t2 - t0) * SOUND_SPEED, (t2 - t1) * SOUND_SPEED, Z)
    x, y = opt.leastsq(
        F, 
        x0=[xp, yp])
    print(time.time() - t)
    print(x,y )