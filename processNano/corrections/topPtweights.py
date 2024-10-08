import numpy as np
import awkward as ak

def topPtWeight(dataset, obj):

    if "ttbar" in dataset:
        print(dataset, "\n")
       
    
        Wp_gen = obj[(obj.status <30) & (obj.status > 20) & (obj.pdgId == 24)]
        Wm_gen = obj[(obj.status <30) & (obj.status > 20) & (obj.pdgId == -24)]
        b_gen  = obj[(obj.status <30) & (obj.status > 20) & (obj.pdgId == 5)]
        ab_gen = obj[(obj.status <30) & (obj.status > 20) & (obj.pdgId == -5)]

        b_gen = b_gen[b_gen.parent.pdgId == 6]
        ab_gen = ab_gen[ab_gen.parent.pdgId == -6]
        Wp_gen = Wp_gen[Wp_gen.parent.pdgId == 6]
        Wm_gen = Wm_gen[Wm_gen.parent.pdgId == -6]

    
        top_pt  = getTopPt(Wp_gen.pt, Wp_gen.eta, Wp_gen.phi, b_gen.pt, b_gen.eta, b_gen.phi)
    
        atop_pt = getTopPt(Wm_gen.pt, Wm_gen.eta, Wm_gen.phi, ab_gen.pt, ab_gen.eta, ab_gen.phi)
    
        pt_Weight = np.sqrt(topPtPowhegMC(top_pt) * topPtPowhegMC(atop_pt))
        return pt_Weight


def getTopPt(Wpt, Weta, Wphi, bPt, bEta, bPhi):
    # Flatten the nested lists to 1D arrays

    Wpt_flat = ak.flatten(Wpt)
    Weta_flat = ak.flatten(Weta)
    Wphi_flat = ak.flatten(Wphi)
    bPt_flat = ak.flatten(bPt)
    bEta_flat = ak.flatten(bEta)
    bPhi_flat = ak.flatten(bPhi)

    Wpt_np = list(filter(lambda item: item is not None, Wpt_flat))
    Wphi_np = list(filter(lambda item: item is not None, Wphi_flat))
    bPt_np = list(filter(lambda item: item is not None, bPt_flat))
    bPhi_np = list(filter(lambda item: item is not None, bPhi_flat))   
 

    # Perform the calculations with the flattened arrays
    Wpx = np.array(Wpt_np) * np.cos(np.array(Wphi_np))
    Wpy = np.array(Wpt_np) * np.sin(np.array(Wphi_np))

    bPx = np.array(bPt_np) * np.cos(np.array(bPhi_np))
    bPy = np.array(bPt_np) * np.sin(np.array(bPhi_np))

    total_px = np.array(Wpx + bPx)
    total_py = np.array(Wpy + bPy)

    total_pt = np.sqrt(total_px * total_px + total_py * total_py)


    return total_pt


#def getTopPt(Wpt, Weta, Wphi, bPt, bEta, bPhi):
#    print(Wpt, "\n")
#    Wpx = Wpt * np.cos(Wphi)
#    Wpy = Wpt * np.sin(Wphi) 
#
#    bPx = bPt * np.cos(bPhi)
#    bPy = bPt * np.sin(bPhi)
#
#    total_px = np.array(Wpx + bPx)
#    total_py = np.array(Wpy + bPy)
#
#    total_pt = np.sqrt(total_px*total_px + total_py*total_py)
#    
#    return total_pt


def topPtPowhegMC(pt):
    return (0.973 - (0.000134 * pt) + (0.103 * np.exp(pt * (-0.0118))))






