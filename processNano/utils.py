import os
import numpy as np
import pandas as pd
#from ROOT import TLorentzVector
#from ROOT import TVector3

def mkdir(path):
    try:
        os.mkdir(path)
    except Exception:
        pass


def p4(obj, is_mc=True):
    result = pd.DataFrame(
        index=obj.index,
        columns=[
            "px",
            "py",
            "pz",
            "px_gen",
            "py_gen",
            "pz_gen",
            "e",
            "e_gen",
            "pt",
            "eta",
            "phi",
            "pt_gen",
            "eta_gen",
            "phi_gen",
            "mass",
            "mass_gen",
            "rap",
        ],
    ).fillna(0.0)
    px_ = obj.pt * np.cos(obj.phi)
    py_ = obj.pt * np.sin(obj.phi)
    pz_ = obj.pt * np.sinh(obj.eta)
    e_ = np.sqrt(px_ ** 2 + py_ ** 2 + pz_ ** 2 + obj.mass ** 2)
    result.px += px_
    result.py += py_
    result.pz += pz_
    result.e += e_
    if is_mc:
        px_gen_ = obj.pt_gen * np.cos(obj.phi_gen)
        py_gen_ = obj.pt_gen * np.sin(obj.phi_gen)
        pz_gen_ = obj.pt_gen * np.sinh(obj.eta_gen)
        e_gen_ = np.sqrt(px_gen_ ** 2 + py_gen_ ** 2 + pz_gen_ ** 2 + obj.mass ** 2)

        result.px_gen += px_gen_
        result.py_gen += py_gen_
        result.pz_gen += pz_gen_
        result.e_gen += e_gen_

    result.pt = np.sqrt(result.px ** 2 + result.py ** 2)
    result.eta = np.arcsinh(result.pz / result.pt)
    result.phi = np.arctan2(result.py, result.px)
    result.mass = np.sqrt(
        result.e ** 2 - result.px ** 2 - result.py ** 2 - result.pz ** 2
    )
    if is_mc:
        result.pt_gen = np.sqrt(result.px_gen ** 2 + result.py_gen ** 2)
        result.eta_gen = np.arcsinh(result.pz_gen / result.pt_gen)
        result.phi_gen = np.arctan2(result.py_gen, result.px_gen)
        result.mass_gen = np.sqrt(
            result.e_gen ** 2
            - result.px_gen ** 2
            - result.py_gen ** 2
            - result.pz_gen ** 2
        )
    result.rap = 0.5 * np.log((result.e + result.pz) / (result.e - result.pz))
    return result


def p4_sum(obj1, obj2, is_mc=True):

    result = pd.DataFrame(
        index=obj1.index.union(obj2.index),
        columns=[
            "px",
            "py",
            "pz",
            "px_gen",
            "py_gen",
            "pz_gen",
            "e",
            "e_gen",
            "pt",
            "eta",
            "phi",
            "pt_gen",
            "eta_gen",
            "phi_gen",
            "mass",
            "mass_gen",
            "rap",
        ],
    ).fillna(0.0)
    for obj in [obj1, obj2]:
        px_ = obj.pt * np.cos(obj.phi)
        py_ = obj.pt * np.sin(obj.phi)
        pz_ = obj.pt * np.sinh(obj.eta)
        e_ = np.sqrt(px_ ** 2 + py_ ** 2 + pz_ ** 2 + obj.mass ** 2)
        result.px += px_
        result.py += py_
        result.pz += pz_
        result.e += e_

#        result.px += px_.reindex(result.index).fillna(0.0)
#        result.py += py_.reindex(result.index).fillna(0.0)
#        result.pz += pz_.reindex(result.index).fillna(0.0)
#        result.e += e_.reindex(result.index).fillna(0.0)


        if is_mc:
            px_gen_ = obj.pt_gen * np.cos(obj.phi_gen)
            py_gen_ = obj.pt_gen * np.sin(obj.phi_gen)
            pz_gen_ = obj.pt_gen * np.sinh(obj.eta_gen)
            e_gen_ = np.sqrt(px_gen_ ** 2 + py_gen_ ** 2 + pz_gen_ ** 2 + obj.mass ** 2)

        if is_mc:
            result.px_gen += px_gen_
            result.py_gen += py_gen_
            result.pz_gen += pz_gen_
            result.e_gen += e_gen_


    result.pt = np.sqrt(result.py.astype(float) ** 2 + result.px.astype(float) ** 2)
    result.eta = np.arcsinh(result.pz.astype(float) / result.pt.astype(float))
#    result.eta = np.arcsinh(result.pz / result.pt)
    result.phi = np.arctan2(result.py.astype(float), result.px.astype(float))
#    result.phi = np.arctan2(result.py, result.px)

    result.e = result.e.astype(float)
    result.px = result.px.astype(float)
    result.py = result.py.astype(float)
    result.pz = result.pz.astype(float)

    result.mass = np.sqrt(
        result.e ** 2 - result.px ** 2 - result.py ** 2 - result.pz ** 2
    )
    if is_mc:
        result.px_gen = result.px_gen.astype(float)
        result.py_gen = result.py_gen.astype(float)
        result.pz_gen = result.pz_gen.astype(float)
        result.e_gen  = result.e_gen.astype(float)
        result.pt_gen = np.sqrt(result.px_gen ** 2 + result.py_gen ** 2)
        result.eta_gen = np.arcsinh(result.pz_gen / result.pt_gen)
        result.phi_gen = np.arctan2(result.py_gen, result.px_gen)
        result.mass_gen = np.sqrt(
            result.e_gen ** 2
            - result.px_gen ** 2
            - result.py_gen ** 2
            - result.pz_gen ** 2
        )
    result.rap = 0.5 * np.log((result.e + result.pz) / (result.e - result.pz))
    return result


def rapidity(obj):
    px = obj.pt * np.cos(obj.phi)
    py = obj.pt * np.sin(obj.phi)
    pz = obj.pt * np.sinh(obj.eta)
    e = np.sqrt(px ** 2 + py ** 2 + pz ** 2 + obj.mass ** 2)
    rap = 0.5 * np.log((e + pz) / (e - pz))
    return rap


def cs_variables_old(mu1, mu2, two_muons):
    dphi = abs(
        np.mod(mu1.phi[two_muons] - mu2.phi[two_muons] + np.pi, 2 * np.pi) - np.pi
    )
    theta_cs = np.arccos(np.tanh((mu1.eta[two_muons] - mu2.eta[two_muons]) / 2))
    phi_cs = np.tan((np.pi - np.abs(dphi)) / 2) * np.sin(theta_cs)
    return np.cos(theta_cs.flatten()), phi_cs.flatten()


# https://root.cern.ch/doc/master/classTVector3
# .html#a5fcc2bc19cf8c84215eb8e50cedae08f
def angle(vec1, vec2):
    ptot2_1 = vec1[0] * vec1[0] + vec1[1] * vec1[1] + vec1[2] * vec1[2]
    ptot2_2 = vec2[0] * vec2[0] + vec2[1] * vec2[1] + vec2[2] * vec2[2]
    ptot2 = ptot2_1 * ptot2_2
    ptot2[ptot2 <= 0] = 0.0
    arg = (vec1[0] * vec2[0] + vec1[1] * vec2[1] + vec1[2] * vec2[2]) / np.sqrt(ptot2)
    arg[arg > 1.0] = 1.0
    arg[arg < -1.0] = -1.0
    return np.arccos(arg)

#def angle(vect1, vect2):
#   
#    result = pd.DataFrame(
#        index = vect1.index.union(vect2.index),
#        columns=[
#            "v1",
#            "v2",
#            "lb_angle",
#        ],
#    ).fillna(0.0)
#
#    px1 = vect1.pt * np.cos(vect1.phi)
#    py1 = vect1.pt * np.sin(vect1.phi)
#    pz1 = vect1.pt * np.sinh(vect1.eta)
#    e1 = np.sqrt(px1 ** 2 + py1 ** 2 + pz1 ** 2 + vect1.mass ** 2)
#
#    px2 = vect2.pt * np.cos(vect2.phi)
#    py2 = vect2.pt * np.sin(vect2.phi)
#    pz2 = vect2.pt * np.sinh(vect2.eta)
#    e2 = np.sqrt(px2 ** 2 + py2 ** 2 + pz2 ** 2 + vect2.mass ** 2)
#
#    pl1  = TLorentzVector()
#    pl2  = TLorentzVector()
#
#    for i in range(len(px1)):
#        pl1.SetPxPyPzE(px1[i], py1[i], pz1[i], e1[i]) 
#        v1_ = TVector3()
#        v1_ = pl1.Vect()
#
#        result.v1 += v1_

#    for i in range(len(px2)):
#        pl2.SetPxPyPzE(px2[i], py2[i], pz2[i], e2[i])
#        v2_ = TVector3()
#        v2_ = pl2.Vect()  
#
#        result.v2 += v2_
#
#    ptot2_1 = v1[0] * v1[0] + v1[1] * v1[1] + v1[2] * v1[2]
#    ptot2_2 = v2[0] * v2[0] + v2[1] * v2[1] + v2[2] * v2[2]
#    ptot2 = ptot2_1 * ptot2_2
#    ptot2[ptot2 <= 0] = 0.0
#    arg = (v1[0] * v2[0] + v1[1] * v2[1] + v1[2] * v2[2]) / np.sqrt(ptot2)
#    arg[arg > 1.0] = 1.0
#    arg[arg < -1.0] = -1.0
#    result.lb_angle = np.arccos(arg)
#        
#    return result

def bbangle(objs1, objs2):
    pt1 = objs1.pt
    eta1 = objs1.eta
    phi1 = objs1.phi
    pt2 = objs2.pt
    eta2 = objs2.eta
    phi2 = objs2.phi
    px1 = pt1 * np.cos(phi1)
    py1 = pt1 * np.sin(phi1)
    pz1 = pt1 * np.sinh(eta1)
    px2 = pt2 * np.cos(phi2)
    py2 = pt2 * np.sin(phi2)
    pz2 = pt2 * np.sinh(eta2)
    ptot2_1 = px1 * px1 + py1 * py1 + pz1 * pz1
    ptot2_2 = px2 * px2 + py2 * py2 + pz2 * pz2
    ptot2 = ptot2_1 * ptot2_2
    ptot2[ptot2 <= 0] = 0.0
    arg = (px1 * px2 + py1 * py2 + pz1 * pz2) / np.sqrt(ptot2)
    #arg[arg > 1.0] = 1.0
    #arg[arg < -1.0] = -1.0
    return np.arccos(arg)
#    return arg

# https://root.cern.ch/doc/master/classTVector3
# .html#a4d0080544bc4d4ac669fa5e3bada8e25
def unit(vec):
    tot2 = vec[0] * vec[0] + vec[1] * vec[1] + vec[2] * vec[2]
    tot = np.ones(len(vec[0]))
    tot[tot2 > 0] = 1 / np.sqrt(tot2[tot2 > 0])
    return [vec[0] * tot, vec[1] * tot, vec[2] * tot]


# https://root.cern.ch/doc/master/classTVector3
# .html#ad4464ec846c85cadce7afe9c09c7e245
def cross(vec1, vec2):
    return [
        vec1[1] * vec2[2] - vec2[1] * vec1[2],
        vec1[2] * vec2[0] - vec2[2] * vec1[0],
        vec1[0] * vec2[1] - vec2[0] * vec1[1],
    ]


# https://root.cern.ch/doc/master/classTLorentzVector
# .html#a8d77f01dc7f409b237937012c382fbfb
def boost(vector, boost_vector):
    x = vector[0]
    y = vector[1]
    z = vector[2]
    t = vector[3]
    bx = boost_vector[0]
    by = boost_vector[1]
    bz = boost_vector[2]
    b2 = bx * bx + by * by + bz * bz
    gamma = 1.0 / np.sqrt(1.0 - b2)
    bp = bx * x + by * y + bz * z
    gamma2 = np.zeros(len(x))
    gamma2[b2 > 0] = (gamma - 1.0) / b2
    x = x + gamma2 * bp * bx + gamma * bx * t
    y = y + gamma2 * bp * by + gamma * by * t
    z = z + gamma2 * bp * bz + gamma * bz * t
    t = gamma * (t + bp)
    return [x, y, z, t]


# https://root.cern.ch/doc/master/classTRotation
# .html#acf7e3da35816052c3b6e73f7fe71239d
def rotate_axes(newX, newY, newZ):
    return [
        [newX[0], newY[0], newZ[0]],
        [newX[1], newY[1], newZ[1]],
        [newX[2], newY[2], newZ[2]],
    ]


# https://root.cern.ch/doc/master/classTRotation
# .html#afe12d186ccecf5d71adea56765021f5c
def multiply_mtx(mtx1, mtx2):
    return [
        [
            mtx1[0][0] * mtx2[0][0] + mtx1[0][1] * mtx2[1][0] + mtx1[0][2] * mtx2[2][0],
            mtx1[0][0] * mtx2[0][1] + mtx1[0][1] * mtx2[1][1] + mtx1[0][2] * mtx2[2][1],
            mtx1[0][0] * mtx2[0][2] + mtx1[0][1] * mtx2[1][2] + mtx1[0][2] * mtx2[2][2],
        ],
        [
            mtx1[1][0] * mtx2[0][0] + mtx1[1][1] * mtx2[1][0] + mtx1[1][2] * mtx2[2][0],
            mtx1[1][0] * mtx2[0][1] + mtx1[1][1] * mtx2[1][1] + mtx1[1][2] * mtx2[2][1],
            mtx1[1][0] * mtx2[0][2] + mtx1[1][1] * mtx2[1][2] + mtx1[1][2] * mtx2[2][2],
        ],
        [
            mtx1[2][0] * mtx2[0][0] + mtx1[2][1] * mtx2[1][0] + mtx1[2][2] * mtx2[2][0],
            mtx1[2][0] * mtx2[0][1] + mtx1[2][1] * mtx2[1][1] + mtx1[2][2] * mtx2[2][1],
            mtx1[2][0] * mtx2[0][2] + mtx1[2][1] * mtx2[1][2] + mtx1[2][2] * mtx2[2][2],
        ],
    ]


# https://root.cern.ch/doc/master/TVector3_8cxx
# .html#aa655a3991b6dd7812fb64735670090c1
def multiply_mtx_vec(mtx, vec):
    return [
        mtx[0][0] * vec[0] + mtx[0][1] * vec[1] + mtx[0][2] * vec[2],
        mtx[1][0] * vec[0] + mtx[1][1] * vec[1] + mtx[1][2] * vec[2],
        mtx[2][0] * vec[0] + mtx[2][1] * vec[1] + mtx[2][2] * vec[2],
    ]


# https://root.cern.ch/doc/master/classTRotation
# .html#a4b2d021944f997bb77a6a29597b2a720
def invert(rot):
    return [
        [rot[0][0], rot[1][0], rot[2][0]],
        [rot[0][1], rot[1][1], rot[2][1]],
        [rot[0][2], rot[1][2], rot[2][2]],
    ]


# https://github.com/arizzi/PisaHmm/blob/master/boost_to_CS.h
def cs_variables(mu1, mu2):

    charge2 = mu2.charge.to_numpy()
    charge1 = mu1.charge.to_numpy()
    eta2 = mu2.eta.to_numpy()
    eta1 = mu1.eta.to_numpy()
    multiplier = charge2
    multiplier[(charge1 != charge2) & (eta1 < eta2)] = -charge1[
        (charge1 != charge2) & (eta1 < eta2)
    ]
    multiplier[(charge1 != charge2) & (eta1 >= eta2)] = charge2[
        (charge1 != charge2) & (eta1 >= eta2)
    ]
    mu1_px = mu1.pt * np.cos(mu1.phi)
    mu1_py = mu1.pt * np.sin(mu1.phi)
    mu1_pz = mu1.pt * np.sinh(mu1.eta)
    mu1_e = np.sqrt(mu1_px ** 2 + mu1_py ** 2 + mu1_pz ** 2 + mu1.mass ** 2)
    mu2_px = mu2.pt * np.cos(mu2.phi)
    mu2_py = mu2.pt * np.sin(mu2.phi)
    mu2_pz = mu2.pt * np.sinh(mu2.eta)
    mu2_e = np.sqrt(mu2_px ** 2 + mu2_py ** 2 + mu2_pz ** 2 + mu2.mass ** 2)
    px = mu1_px + mu2_px
    py = mu1_py + mu2_py
    pz = mu1_pz + mu2_pz
    e = mu1_e + mu2_e

    mu1_kin = [mu1_px, mu1_py, mu1_pz, mu1_e]
    mu2_kin = [mu2_px, mu2_py, mu2_pz, mu2_e]
    pf = (
        np.full(len(px), 0),
        np.full(len(px), 0),
        np.full(len(px), -6500),
        np.full(len(px), 6500),
    )
    pw = (
        np.full(len(px), 0),
        np.full(len(px), 0),
        np.full(len(px), 6500),
        np.full(len(px), 6500),
    )
    boost_vector = [-px / e, -py / e, -pz / e]

    mu1_kin = boost(mu1_kin, boost_vector)
    mu2_kin = boost(mu2_kin, boost_vector)
    pf = boost(pf, boost_vector)
    pw = boost(pw, boost_vector)
#    angle_filter = angle([px, py, pz], [pf[0], pf[1], pf[2]]) < angle(
#        [px, py, pz], [pw[0], pw[1], pw[2]]
#    )
#    for i in range(4):
#        pw[i][angle_filter] = -multiplier[angle_filter] * pw[i][angle_filter]
#        pf[i][angle_filter] = multiplier[angle_filter] * pf[i][angle_filter]
#        pf[i][~angle_filter] = -multiplier[~angle_filter] * pf[i][~angle_filter]
#        pw[i][~angle_filter] = multiplier[~angle_filter] * pw[i][~angle_filter]

    pf_mag = np.sqrt(pf[0] * pf[0] + pf[1] * pf[1] + pf[2] * pf[2])
    pw_mag = np.sqrt(pw[0] * pw[0] + pw[1] * pw[1] + pw[2] * pw[2])
    for i in range(4):
        pf[i] = pf[i] / pf_mag
        pw[i] = pw[i] / pw_mag

    pbisec = [pf[0] + pw[0], pf[1] + pw[1], pf[2] + pw[2], pf[3] + pw[3]]
    phisecz = unit([pbisec[0], pbisec[1], pbisec[2]])
    phisecy = unit(cross(phisecz, unit([px, py, pz])))

    muminus = [mu2_kin[0], mu2_kin[1], mu2_kin[2]]
    rotation = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    rot_axes = rotate_axes(cross(phisecy, phisecz), phisecy, phisecz)
    rotation = multiply_mtx(rot_axes, rotation)
    rotation = invert(rotation)
    muminus = multiply_mtx_vec(rotation, muminus)
    theta_cs = np.arctan2(
        np.sqrt(muminus[0] * muminus[0] + muminus[1] * muminus[1]), muminus[2]
    )
    cos_theta_cs = np.cos(theta_cs)
    phi_cs = np.arctan2(muminus[1], muminus[0])
    return cos_theta_cs, phi_cs


def delta_r(eta1, eta2, phi1, phi2):
    deta = abs(eta1 - eta2)
    dphi = abs(np.mod(phi1 - phi2 + np.pi, 2 * np.pi) - np.pi)
    dr = np.sqrt(deta ** 2 + dphi ** 2)
    return deta, dphi, dr

def overlap_removal(obj1, obj2):

    eta1 = obj1.eta
    phi1 = obj1.phi   

    if len(obj2) == 0:
        # if there are no electrons, return an empty array of zeros
        return np.zeros_like(eta1)

    eta2 = obj2.iloc[0].eta  
    phi2 = obj2.iloc[0].phi


    deta = abs(eta1 - eta2)
    dphi = abs(np.mod(phi1 - phi2 + np.pi, 2 * np.pi) - np.pi)
    dr = np.sqrt(deta ** 2 + dphi ** 2)

#    value_temp = dr.loc[dr <= 1.0]
#    print("--testing-- ", value_temp)

    return dr
