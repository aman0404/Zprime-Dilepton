import numpy as np
import awkward as ak

ttbar_wgts = 1.0
def ttbar_sf(df):
    year    = df.year
    dataset = df.dataset
    nbjets = df.nbjets
    regions = df.regions
    if "ttbar" in dataset:
       if year == 2018:
          #print(dataset, "\n")
          if regions == "bb":
  
             if nbjets == 0:
                 ttbar_wgts = 0.84
             elif nbjets == 1:
                 ttbar_wgts = 0.85
             elif nbjets == 2:
                 ttbar_wgts = 0.83
             else:
                 ttbar_wgts = 1.38
  
          elif regions == "be":
             if nbjets == 0:
                 ttbar_wgts = 1.00
             elif nbjets == 1:
                 ttbar_wgts = 0.95
             elif nbjets == 2:
                 ttbar_wgts = 0.91
             else:
                 ttbar_wgts = 1.40         
          else:
                 ttbar_wgts = 1.0

       if year == 2017:
          #print(dataset, "\n")
          if regions == "bb":

             if nbjets == 0:
                 ttbar_wgts = 0.83
             elif nbjets == 1:
                 ttbar_wgts = 0.83
             elif nbjets == 2:
                 ttbar_wgts = 0.81
             else:
                 ttbar_wgts = 1.15

          elif regions == "be":
             if nbjets == 0:
                 ttbar_wgts = 1.04
             elif nbjets == 1:
                 ttbar_wgts = 0.93
             elif nbjets == 2:
                 ttbar_wgts = 0.88
             else:
                 ttbar_wgts = 1.26
          else:
                 ttbar_wgts = 1.0

       if year == 2016:
          #print(dataset, "\n")
          if regions == "bb":

             if nbjets == 0:
                 ttbar_wgts = 0.92
             elif nbjets == 1:
                 ttbar_wgts = 0.83
             elif nbjets == 2:
                 ttbar_wgts = 0.84
             else:
                 ttbar_wgts = 1.37

          elif regions == "be":
             if nbjets == 0:
                 ttbar_wgts = 1.10
             elif nbjets == 1:
                 ttbar_wgts = 0.93
             elif nbjets == 2:
                 ttbar_wgts = 0.94
             else:
                 ttbar_wgts = 1.54
          else:
                 ttbar_wgts = 1.0
    else:
        ttbar_wgts = 1.0

    return ttbar_wgts
