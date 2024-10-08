from config.parameters import parameters
import correctionlib
import numpy as np
import pandas as pd
import awkward  as ak


def musf_evaluator(parameters, year, mu1, mu2):


    scaleFactors = parameters["muSFFileList"]
    id_file = scaleFactors[0]['id']

    muon_correctionset = correctionlib.CorrectionSet.from_file(
        id_file[0]
    )
    print(id_file) 
    
    sf = pd.DataFrame(
        index=mu1.index,
        columns=[
            "muID_nom",
            "muID_up",
            "muID_down",
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

    sf["muID_nom"] *= ak.to_numpy(muID_)
    sf["muID_up"] *= ak.to_numpy(muIDUp_)
    sf["muID_down"] *= ak.to_numpy(muIDDown_)

    muID = {"nom": sf["muID_nom"], "up": sf["muID_up"], "down": sf["muID_down"]}

    return muID
    
