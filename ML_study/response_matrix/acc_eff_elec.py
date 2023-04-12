import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math

p0 = 0.576
p1 = -417.7
p2 = 381.8
p3 = 4.607e04
p4 = 1.072e05

def value(m):
    value = p0 + p1 / (m+p2) + p3/((m*m)+p4)
    return value

p0be = 0.01443
p1be = 475.7
p2be = 639.1
p3be = -1.056e05
p4be = 8.281e04
p5be = 1.289e07
p6be = 2.317e07

def be_value(m):
    bevalue = p0be + p1be / (m+p2be) + p3be/((m*m)+p4be) + p5be/ (m**3 +p6be)
    return bevalue
