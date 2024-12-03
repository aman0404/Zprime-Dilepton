# ZPrimeCombine
Tools to perform statistical analyses for the Z' -> ll analysis using the Higgs combine toolkit

## Current combine installation recipe:
```
 
cmsrel CMSSW_14_1_0_pre4
cd CMSSW_14_1_0_pre4/src
cmsenv
git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
cd HiggsAnalysis/CombinedLimit

cd $CMSSW_BASE/src/HiggsAnalysis/CombinedLimit
git fetch origin
git checkout v10.0.2
scramv1 b clean; scramv1 b # always make a clean build

git clone https://github.com/cms-analysis/CombineHarvester.git CombineHarvester
scram b
```

## Check out ZPrimeCombine toolkit:
```
   git clone https://USERNAME@gitlab.cern.ch/cms-zprime-dileptons/ZPrimeCombine.git
   cd ZPrimeCombine
   git fetch 
   git checkout dileptonPlusB 
```

## General considerations:  
This repository consits of python scripts fulfilling two purposes:

1) Create datacards and ROOT files containing workspaces as input for combine,

2) Serve as a user-friendly interface to execute combine in the appropriate configuration for limits and p-values/significance,

For detailed instructions on usage, please see the manual in the documentation folder

## Example commands for dilepton + b-jets:

Write datacards for bbll model:

`python runInterpretation.py -c 2LB -t test --BBLL -w`

Write datacards for bsll model:

`python runInterpretation.py -c 2LB -t test --BSLL -w`

 - To execute the calculation, remove the `-w`
 - To re-write the datacards and execute the calculation, add `-r`
 - To run expected limits, add `-e`
 - To submit calculations to the cluster, add `-s`
