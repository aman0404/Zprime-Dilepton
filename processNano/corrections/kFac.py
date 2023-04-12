import numpy as np


def calckFac(mass, region, flavor):

    if flavor == "mu":
        if region == "all":
            pars = [
                1.053,
                -0.0001552,
                5.661e-08,
                -8.382e-12,
            ]
        elif region == "bb":
            pars = [
                1.032,
                -0.000138,
                4.827e-08 ,
                -7.321e-12,
            ]
        elif region == "be":
            pars = [
                1.064,
                -0.0001674,
                6.599e-08,
                -9.657e-12,
            ]
        if mass < 150:
            correction = 1
        else:
            correction = pars[0]
            for i in range(1, 4):
                correction += pars[i] * mass ** i

    else:

        pars = [1.0678, -0.000120666, 3.22646e-08, -3.94886e-12]
        if mass < 120:
            correction = 1
        else:
            correction = pars[0]
            for i in range(1, 3):
                correction += pars[i] * mass ** i

    return correction


def kFac(masses, region, flavor):

    result = [calckFac(mass, region, flavor) for mass in masses]
    return np.array(result)
