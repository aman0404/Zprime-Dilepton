from config.parameters import parameters
import correctionlib
import numpy as np
import pandas as pd
import awkward  as ak


def musf_hlt_evaluator(parameters, year, mu1, mu2):


    scaleFactors = parameters["muSFFileList"]
    id_file = scaleFactors[0]['HLT']

    muon_correctionset = correctionlib.CorrectionSet.from_file(
        id_file[0]
    )
    print(id_file) 
    
    sf = pd.DataFrame(
        index=mu1.index,
        columns=[
            "muHLT_nom",
            "muHLT_up",
            "muHLT_down",
        ],
    )
    sf = sf.fillna(1.0)  

    for mu in [mu1, mu2]:
        pt = mu.pt.values
        eta = mu.eta_raw.values
        abs_eta = abs(mu.eta_raw.values)

    muID_ = muon_correctionset[id_file[1]].evaluate(
         np.abs(eta), np.abs(pt), "nominal"
    )
    muIDUp_ = muon_correctionset[id_file[1]].evaluate(
         np.abs(eta), np.abs(pt), "systup"
    )
    muIDDown_ = muon_correctionset[id_file[1]].evaluate(
         np.abs(eta), np.abs(pt), "systdown"
    )

    sf["muHLT_nom"] *= ak.to_numpy(muID_)
    sf["muHLT_up"] *= ak.to_numpy(muIDUp_)
    sf["muHLT_down"] *= ak.to_numpy(muIDDown_)

    muID = {"nom": sf["muHLT_nom"], "up": sf["muHLT_up"], "down": sf["muHLT_down"]}

    return muID
    
