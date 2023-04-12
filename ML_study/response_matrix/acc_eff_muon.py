import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math

p0 = 2.14
p1 = 0.1286
p2 = 110.6
p3 = 22.44
p4 = -2.366
p5 = -0.03382

p00 = 5.18
p11 = -5.845e04
p22 = 1.157e04
p33 = 0.0002255

def value(m):
    value = p0 - p1 * (math.exp(-(m-p2)/p3)) + p4* (m**p5)
    return value

def highmass(m):
    highvalue = p00 + p11/(m+p22) - p33*m
    return highvalue

def cal_eff(m):

    if m < 600.:
       ans = value(m)
    else:
       ans = highmass(m)
    return ans

p0be = 13.4
p1be = 6.693
p2be = -4.852e06
p3be = -7.437e06
p4be = -81.43
p5be = -1.068

p00be = 0.3154
p11be = 0.04561
p22be = 1.362
p33be = -4927
p44be = 727.5

def be_value(m):
    bevalue = p0be - p1be * (math.exp(-(m-p2be)/p3be)) + p4be* (m**p5be)
    return bevalue

def be_highmass(m):
    be_hm = p00be + p11be* (m**p22be)* math.exp(-(m-p33be)/p44be)
    return be_hm

def be_cal_eff(m):

    if m < 450.:
       ans = be_value(m)
    else:
       ans = be_highmass(m)
    return ans

       
