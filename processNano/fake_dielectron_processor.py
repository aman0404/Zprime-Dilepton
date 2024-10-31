import sys

sys.path.append("copperhead/")

import awkward
import awkward as ak
import numpy as np

import pandas as pd
import coffea.processor as processor
#from coffea.lookup_tools import extractor
from coffea.lumi_tools import LumiMask
from processNano.timer import Timer
from processNano.weights import Weights

from config.parameters import parameters, ele_branches, jet_branches, muon_branches
from copperhead.stage1.corrections.pu_reweight import pu_lookups, pu_evaluator
from copperhead.stage1.corrections.l1prefiring_weights import l1pf_weights
from processNano.electrons import find_dielectron, fill_electrons
from processNano.jets import prepare_jets, fill_jets, fill_bjets, btagSF

import copy
from processNano.corrections.nnpdfWeight import NNPDFWeight
from processNano.corrections.kFac import kFac
from processNano.corrections.jec import jec_factories, apply_jec
#from copperhead.stage1.corrections.jec import jec_factories, apply_jec

from processNano.utils import overlap_removal

##top pT reweighting
from processNano.corrections.topPtweights import topPtWeight

#fake background estimation
#from processNano.corrections.fake_factors import calculate_fakes
from processNano.corrections.fake_factors_v7 import calculate_fakes_v7

class DielectronProcessor(processor.ProcessorABC):
    def __init__(self, **kwargs):
        self.samp_info = kwargs.pop("samp_info", None)
        do_timer = kwargs.pop("do_timer", True)
        self.apply_to_output = kwargs.pop("apply_to_output", None)
        self.pt_variations = kwargs.pop("pt_variations", ["nominal"])

        self.years = self.samp_info.years

        if(self.years == '2016pre' or self.years == '2016post'):
           self.year = '2016'
        else:
           self.year = self.years
        self.parameters = {k: v.get(self.years, None) for k, v in parameters.items()}
        print("Processing ", self.year, self.years)
        self.do_btag = True

        if self.samp_info is None:
            print("Samples info missing!")
            return

        self._accumulator = processor.defaultdict_accumulator(int)

        self.applykFac = False
        self.applyNNPDFWeight = False

        self.applyTopPtWeight = True
        self.calc_fake = True
        self.do_pu = True
        self.auto_pu = True
        self.do_l1pw = True  # L1 prefiring weights
        self.do_jecunc = True
        self.do_jerunc = False
        
        self.timer = Timer("global") if do_timer else None
        
        self._columns = self.parameters["proc_columns"]

        self.regions = ["bb", "be"]
        self.channels = ["mumu"]
        

        self.lumi_weights = self.samp_info.lumi_weights
        
        self.prepare_lookups()


    @property
    def accumulator(self):
        return self._accumulator

    @property
    def columns(self):
        return self._columns

    def process(self, df):

        # Initialize timer
        if self.timer:
            self.timer.update()

        # Dataset name (see definitions in config/datasets.py)
        dataset = df.metadata["dataset"]

        is_mc = True
        if "data" in dataset:
            is_mc = False

        # ------------------------------------------------------------#
        # Apply HLT, lumimask, genweights, PU weights
        # and L1 prefiring weights
        # ------------------------------------------------------------#

        numevents = len(df)

        # All variables that we want to save
        # will be collected into the 'output' dataframe
        output = pd.DataFrame(
            {"run": df.run, "event": df.event, "luminosityBlock": df.luminosityBlock}
        )
        output.index.name = "entry"
        output["npv"] = df.PV.npvs
        output["met"] = df.MET.pt

        # Separate dataframe to keep track on weights
        # and their systematic variations
        weights = Weights(output)
        ele_branches_local = copy.copy(ele_branches)

        if is_mc:
            genPart = df.GenPart
            genPart = genPart[
                (
                    (abs(genPart.pdgId) == 11) | abs(genPart.pdgId)
                    == 13 | (abs(genPart.pdgId) == 15)
                )
                & genPart.hasFlags(["isHardProcess", "fromHardProcess", "isPrompt"])
            ]

            cut = ak.num(genPart) == 2
            output["dielectron_mass_gen"] = cut
            output["dielectron_pt_gen"] = cut
            output["dielectron_eta_gen"] = cut
            output["dielectron_phi_gen"] = cut
            genMother = genPart[cut][:, 0] + genPart[cut][:, 1]
            output.loc[
                output["dielectron_mass_gen"] == True, ["dielectron_mass_gen"]
            ] = genMother.mass
            output.loc[
                output["dielectron_pt_gen"] == True, ["dielectron_pt_gen"]
            ] = genMother.pt
            output.loc[
                output["dielectron_eta_gen"] == True, ["dielectron_eta_gen"]
            ] = genMother.eta
            output.loc[
                output["dielectron_phi_gen"] == True, ["dielectron_phi_gen"]
            ] = genMother.phi
            output.loc[output["dielectron_mass_gen"] == False, ["dielectron_mass_gen"]] = -999.0
            output.loc[output["dielectron_pt_gen"] == False, ["dielectron_pt_gen"]] = -999.0
            output.loc[output["dielectron_eta_gen"] == False, ["dielectron_eta_gen"]] = -999.0
            output.loc[output["dielectron_phi_gen"] == False, ["dielectron_phi_gen"]] = -999.0

        else:
            output["dielectron_mass_gen"] = -999.0
            output["dielectron_pt_gen"] = -999.0
            output["dielectron_eta_gen"] = -999.0
            output["dielectron_phi_gen"] = -999.0

        output["dielectron_mass_gen"] = output["dielectron_mass_gen"].astype(float)
        output["dielectron_pt_gen"] = output["dielectron_pt_gen"].astype(float)
        output["dielectron_eta_gen"] = output["dielectron_eta_gen"].astype(float)
        output["dielectron_phi_gen"] = output["dielectron_phi_gen"].astype(float)
        

            

        if is_mc:
            # For MC: Apply gen.weights, pileup weights, lumi weights,
            # L1 prefiring weights
            mask = np.ones(numevents, dtype=bool)
            genPart = df.GenPart

            genweight = df.genWeight
            weights.add_weight("genwgt", genweight)
            weights.add_weight("lumi", self.lumi_weights[dataset])
            if self.do_pu:
                pu_wgts = pu_evaluator(
                    self.pu_lookups,
                    self.parameters,
                    numevents,
                    np.array(df.Pileup.nTrueInt),
                    self.auto_pu,
                )
                weights.add_weight("pu_wgt", pu_wgts, how="all")


            if self.applyTopPtWeight:
                    topPtweight = topPtWeight(dataset, genPart)
                    weights.add_weight("topPt", topPtweight)

            if self.do_l1pw:
                if self.parameters["do_l1prefiring_wgts"]:
                    if "L1PreFiringWeight" in df.fields:
                        l1pfw = l1pf_weights(df)
                        weights.add_weight("l1prefiring_wgt", l1pfw, how="all")
                    else:
                        weights.add_weight("l1prefiring_wgt", how="dummy_vars")

            df["Electron", "pt_gen"] = df.Electron.matched_gen.pt
            df["Electron", "eta_gen"] = df.Electron.matched_gen.eta
            df["Electron", "phi_gen"] = df.Electron.matched_gen.phi
            df["Electron", "idx"] = df.Electron.genPartIdx
            ele_branches_local += ["genPartFlav", "pt_gen", "eta_gen", "phi_gen", "idx"]
        else:
            # For Data: apply Lumi mask
            lumi_info = LumiMask(self.parameters["lumimask_UL_el"])
            mask = lumi_info(df.run, df.luminosityBlock)
        # Apply HLT to both Data and MC
        hlt = ak.to_pandas(df.HLT[self.parameters["el_hlt"]])
        hlt = hlt[self.parameters["el_hlt"]].sum(axis=1)

        if self.timer:
            self.timer.add_checkpoint("Applied HLT and lumimask")

##Aman edits
        muon_branches_local = copy.copy(muon_branches)
        df["Muon", "pt_raw"] = df.Muon.pt
        df["Muon", "eta_raw"] = df.Muon.eta
        df["Muon", "phi_raw"] = df.Muon.phi

        muons = ak.to_pandas(df.Muon[muon_branches_local])
        muons = muons.dropna()
        muons = muons.loc[:, ~muons.columns.duplicated()]

        muons["selection"] = 0

        

        # Save raw variables before computing any corrections

        df["Electron", "pt_raw"] = df.Electron.pt
        df["Electron", "eta_raw"] = df.Electron.eta
        df["Electron", "phi_raw"] = df.Electron.phi

        if True:  # indent reserved for loop over pT variations

            # --- conversion from awkward to pandas --- #
            electrons = ak.to_pandas(df.Electron[ele_branches_local])
            electrons.pt = electrons.pt_raw * (electrons.scEtOverPt + 1.0)
            electrons.eta = electrons.eta_raw + electrons.deltaEtaSC
            electrons = electrons.dropna()
            electrons = electrons.loc[:, ~electrons.columns.duplicated()]
            if is_mc:
                electrons.loc[electrons.idx == -1, "pt_gen"] = -999.0
                electrons.loc[electrons.idx == -1, "eta_gen"] = -999.0
                electrons.loc[electrons.idx == -1, "phi_gen"] = -999.0

            if self.timer:
                self.timer.add_checkpoint("load electron data")

            #Aman edits
            muons["veto"] = 0
            muons.loc[((muons.pt > 10.)
                & (abs(muons.eta) < 2.4)
                & (muons[self.parameters["muon_id"]] > 0)),
                "veto",
            ] = 1

            # --------------------------------------------------------#
            # Electron selection
            # --------------------------------------------------------#

            # Apply event quality flag
            flags = ak.to_pandas(df.Flag)
            flags = flags[self.parameters["event_flags"]].product(axis=1)


            
            electrons["overlap"] = (overlap_removal(electrons, muons))

            electrons["overlap"].fillna(1., inplace=True)

            # Define baseline electron selection (applied to pandas DF!)
            electrons["selection"] = (
                (electrons.pt > self.parameters["electron_pt_cut"])
                & (abs(electrons.eta) < self.parameters["electron_eta_cut"])
                & (((abs(electrons.dxy) < 0.02) & (abs(electrons.eta) < 1.4442))
                   | ((abs(electrons.dxy) < 0.05) & ((abs(electrons.eta) > 1.566) & (abs(electrons.eta) < 2.5))))                
                & (((abs(electrons.hoe) < 0.15) & (abs(electrons.eta) < 1.4442))
                   | ((abs(electrons.hoe) < 0.10) & ((abs(electrons.eta) > 1.566) & (abs(electrons.eta) < 2.5))))
                & (((abs(electrons.sieie) < 0.013) & (abs(electrons.eta) < 1.4442))
                   | ((abs(electrons.sieie) < 0.034) & ((abs(electrons.eta) > 1.566) & (abs(electrons.eta) < 2.5))))
                & (electrons.lostHits <= 1)   
 
                #& (electrons[self.parameters["electron_id"]] > 0)
            )
      
    
            #if dataset == "dyInclusive50":
            #    electrons = electrons[electrons.genPartFlav == 15]
            
            electrons["pass_flags"] = True
            if self.parameters["electron_flags"]:
                electrons["pass_flags"] = electrons[self.parameters["electron_flags"]].product(
                   axis=1
                )

            # Count electrons
            nelectrons = (
                electrons[electrons.selection]
                .reset_index()
                .groupby("entry")["subentry"]
                .nunique()
            )
            
            #charge on electrons
            sum_charge = electrons.loc[electrons.selection, "charge"].groupby("entry").sum()
 
            #print(sum_charge)

            #print(electrons.charge)
            good_pv = ak.to_pandas(df.PV).npvsGood > 0
            output["event_selection"] = (
                mask
                & (hlt > 0)
                & (flags>0)
                & (nelectrons >= 2)
                #& (abs(sum_charge) >= 2)
                & (good_pv)
                )

            
           
            if self.timer:
                self.timer.add_checkpoint("Selected events and electrons")

            # --------------------------------------------------------#
            # Initialize electron variables
            # --------------------------------------------------------#

            electrons = electrons.join(muons["veto"])
            electrons["veto"] = electrons["veto"].fillna(0)

            
            #electrons = electrons[electrons.selection & (nelectrons >= 2) & (hlt > 0) & (abs(sum_charge) == 2) & (good_pv) ]
            electrons = electrons[electrons.selection & (nelectrons >= 2) & (hlt > 0) ]
            
            #print("electrons ", electrons) 

            nmuons = electrons.loc[:, "veto"].groupby("entry").sum()
            #electrons = electrons[electrons.selection & (nelectrons >= 2) & (hlt > 0) & (abs(sum_charge) == 2) & (good_pv) & (nmuons==0)]
            electrons = electrons[electrons.selection & (nelectrons >= 2) & (hlt > 0) & (good_pv) & (nmuons==0)]


            if self.timer:
                self.timer.add_checkpoint("electron object selection")

            output["r"] = None
            output["dataset"] = dataset
            output["year"] = self.year

            if electrons.shape[0] == 0:
                output = output.reindex(sorted(output.columns), axis=1)
                output = output[output.r.isin(self.regions)]


                if self.apply_to_output is None:
                    return output
                else:
                    self.apply_to_output(output)
                    return self.accumulator.identity()

            result = electrons.groupby("entry").apply(find_dielectron, is_mc=is_mc)
            if is_mc:
                dielectron = pd.DataFrame(
                    result.to_list(), columns=["idx1", "idx2", "mass", "mass_gen"]
                )
            else:
                dielectron = pd.DataFrame(
                    result.to_list(), columns=["idx1", "idx2", "mass"]
                )
            e1 = electrons.loc[dielectron.idx1.values, :]
            e2 = electrons.loc[dielectron.idx2.values, :]
            e1.index = e1.index.droplevel("subentry")
            e2.index = e2.index.droplevel("subentry")

            
            #e1 = e1.join(output["run"])
            #.rename(columns={"run": "run_no"}))
            #e1["run"] = e1["run"].fillna(0)
           
            #print("sum charge is \n", sum_charge, nelectrons) 
            #print(e1.cutBased_HEEP, e1.charge,  "\n")
            #print(e2.cutBased_HEEP, e2.charge, "\n")


            ##e1 preselections 
            e1["pre_selections"] = ( 
                (((abs(e1.dxy) < 0.02) & (abs(e1.eta) < 1.4442))
                   | ((abs(e1.dxy) < 0.05) & ((abs(e1.eta) > 1.566) & (abs(e1.eta) < 2.5))))
                   & (((abs(e1.hoe) < 0.15) & (abs(e1.eta) < 1.4442))
                   | ((abs(e1.hoe) < 0.10) & ((abs(e1.eta) > 1.566) & (abs(e1.eta) < 2.5))))
                   & (((abs(e1.sieie) < 0.013) & (abs(e1.eta) < 1.4442))
                   | ((abs(e1.sieie) < 0.034) & ((abs(e1.eta) > 1.566) & (abs(e1.eta) < 2.5))))
                   & (e1.lostHits <= 1)
                   )

            ## e2 preselections

            e2["pre_selections"] = (
                (((abs(e2.dxy) < 0.02) & (abs(e2.eta) < 1.4442))
                   | ((abs(e2.dxy) < 0.05) & ((abs(e2.eta) > 1.566) & (abs(e2.eta) < 2.5))))
                   & (((abs(e2.hoe) < 0.15) & (abs(e2.eta) < 1.4442))
                   | ((abs(e2.hoe) < 0.10) & ((abs(e2.eta) > 1.566) & (abs(e2.eta) < 2.5))))
                   & (((abs(e2.sieie) < 0.013) & (abs(e2.eta) < 1.4442))
                   | ((abs(e2.sieie) < 0.034) & ((abs(e2.eta) > 1.566) & (abs(e2.eta) < 2.5))))
                   & (e2.lostHits <= 1)
                   )


            #print("hello")
            #print(e1.pre_selections, "\n")            
            #print(e2.pre_selections, "\n")            

            if self.timer:
                self.timer.add_checkpoint("dielectron pair selection")

            if self.timer:
                self.timer.add_checkpoint("back back angle calculation")
            dielectron_mass = dielectron.mass


            output["event_selection"] = ((output.event_selection) & (nmuons==0))
           
            #electrons["run_no"] = output["run"].loc[electrons.index.get_level_values(0)].values 
            #print("fake background estimation before /n")
            #print(electrons.columns)            
            FR_val = 1.0
            output["fake_wgt"] = 1.0
            
            if ((self.calc_fake == True)):
            #if (("data" in dataset) and (self.calc_fake == True)):
                #new_output = output[output.event_selection]
                #run_no = new_output.run
                #run_no = e1.run
                #for fake rate estimation
                #e1["FR1"] =  ((e1.cutBased_HEEP == False) & (e2.cutBased_HEEP == True))
                #e1["FR2"] =  ((e1.cutBased_HEEP == True)  & (e2.cutBased_HEEP == False))
                #e1["FR12"] = ((e1.cutBased_HEEP == False) & (e2.cutBased_HEEP == False))
                #e1["no_FR"] = ((e1.cutBased_HEEP == True) & (e2.cutBased_HEEP == True))

                #for fake bkg estimation
                e1["FR1"] =  ((e1.cutBased_HEEP == False) & (e1.pre_selections == True) & (e2.cutBased_HEEP == True))
                e1["FR2"] =  ((e2.cutBased_HEEP == False) & (e2.pre_selections == True) & (e1.cutBased_HEEP == True))

                e1["FR12"] = ((e2.cutBased_HEEP == False) & (e2.pre_selections == True) & (e1.cutBased_HEEP == False) 
                              & (e1.pre_selections == True))

                e1["no_FR"] = ((e2.cutBased_HEEP == True) & (e2.pre_selections == True) 
                              & (e1.cutBased_HEEP == True)
                              & (e1.pre_selections == True))


                #new_output["FR12"] = ((e1.cutBased_HEEP == False) & (e2.cutBased_HEEP == False))
                #new_output["FR2"] = ((e1.cutBased_HEEP == True) & (e2.cutBased_HEEP == False))
                #new_output["no_FR"] = ((e1.cutBased_HEEP == True) & (e2.cutBased_HEEP == True))
                #new_output["FR12"] = ((e1.cutBased_HEEP == False) & (e2.cutBased_HEEP == False))
                #print(new_output.FR1, "\n")
                #print(new_output.FR2, "\n")
                #print(new_output.no_FR, "\n")
                #print(new_output.FR12, "\n")
                
                for index, row in e1.iterrows():
                    #print(e2.pt[index])
                    #print(e2.eta[index])
                    #print(e2.phi[index])

                    if row['no_FR'] == True:
                        FR_val = 0.


                    if row['FR1'] == True:
                        #FR_val1 = calculate_fakes(run_no[index], e1.pt[index], e1.eta[index], e1.phi[index])
                        FR_val1 = calculate_fakes_v7(e1.pt[index], e1.eta[index])

                        #FR_val = (FR_val1/(1 - FR_val1)) * (1/(1 - FR_val1))
                        #FR_val = FR_val1/(1 - FR_val1)
                        FR_val = 0.
                        #print("this is working 1 \n")
                    if(row['FR2'] == True):
                        #FR_val2 = calculate_fakes(run_no[index], e2.pt[index], e2.eta[index], e2.phi[index])
                        FR_val2 = calculate_fakes_v7(e2.pt[index], e2.eta[index])
                        #FR_val = (FR_val2/(1 - FR_val2)) * (1/(1 - FR_val2))
                        #FR_val = FR_val2/(1 - FR_val2)
                        FR_val = 0.

                        #print("this is working 2 \n")
                    if(row['FR12'] == True):
                      #FR_val1 = calculate_fakes(run_no[index], e1.pt[index], e1.eta[index], e1.phi[index])
                        FR_val1 = calculate_fakes_v7(e1.pt[index], e1.eta[index])
                      #FR_val2 = calculate_fakes(run_no[index], e2.pt[index], e2.eta[index], e2.phi[index])
                        FR_val2 = calculate_fakes_v7(e2.pt[index], e2.eta[index])
                      #FR_val = ((FR_val1/(1 - FR_val1))*(1/(1 - FR_val1))) * ((FR_val2/(1 - FR_val2)) * (1/(1 - FR_val2)))
                        FR_val = (FR_val1/(1 - FR_val1)) * (FR_val2/(1 - FR_val2))
                        #print("this is working 3 \n")

                        #FR_val = 0.
                    #print("value is ", FR_val)
                    output.fake_wgt[index] = FR_val
            
            weights.add_weight('fake_wgt', output.fake_wgt)
                    
                   
            
            # output["fake_wgt"] = 0.0
            # if (("data" in dataset) and (self.calc_fake == True)):
            #     print("fake background estimation /n")
            #     new_output = output.event_selection
            #     run_no = new_output.run
            #     output.fake_wgt = calculate_fakes(run_no, electrons)
            #     print(output.fake_wgt, electrons.pt, electrons.eta, electrons.phi)
                
                
            # --------------------------------------------------------#
            # Select events with muons passing leading pT cut
            # and trigger matching
            # --------------------------------------------------------#

            # Events where there is at least one muon passing
            # leading muon pT cut
            # if self.timer:
            #    self.timer.add_checkpoint("Applied trigger matching")

            # --------------------------------------------------------#
            # Fill dielectron and electron variables
            # --------------------------------------------------------#

            fill_electrons(output, e1, e2, is_mc)

            if self.timer:
                self.timer.add_checkpoint("all electron variables")

        # ------------------------------------------------------------#
        # Prepare jets
        # ------------------------------------------------------------#

        prepare_jets(df, is_mc)

        # ------------------------------------------------------------#
        # Apply JEC, get JEC and JER variations
        # ------------------------------------------------------------#

        jets = df.Jet

        self.do_jec = True

        # We only need to reapply JEC for 2018 data
        # (unless new versions of JEC are released)
#        if ("data" in dataset) and ("2018" in self.year):
#            self.do_jec = False

        jets = apply_jec(
            df,
            jets,
            dataset,
            is_mc,
            self.years,
            self.do_jec,
            self.do_jecunc,
            self.do_jerunc,
            self.jec_factories,
            self.jec_factories_data,
        )
        output.columns = pd.MultiIndex.from_product(
            [output.columns, [""]], names=["Variable", "Variation"]
        )

        if self.timer:
            self.timer.add_checkpoint("Jet preparation & event weights")

        for v_name in self.pt_variations:
            output_updated = self.jet_loop(
                v_name,
                is_mc,
                df,
                dataset,
                mask,
                electrons,
                e1,
                e2,
                jets,
                jet_branches,
                weights,
                numevents,
                output,
            )
            if output_updated is not None:
                output = output_updated

        if self.timer:
            self.timer.add_checkpoint("Jet loop")
        # ------------------------------------------------------------#
        # Calculate other event weights
        # ------------------------------------------------------------#

        """
        if is_mc:
            do_zpt = ('dy' in dataset)
            if do_zpt:
                zpt_weight = np.ones(numevents, dtype=float)
                zpt_weight[two_muons] =\
                    self.evaluator[self.zpt_path](
                        output['dimuon_pt'][two_muons]
                    ).flatten()
                weights.add_weight('zpt_wgt', zpt_weight)

        if self.timer:
            self.timer.add_checkpoint("Computed event weights")
        """

        # ------------------------------------------------------------#
        # Fill outputs
        # ------------------------------------------------------------#
        # mass = output.dielectron_mass
        output["r"] = None
        output.loc[
            ((abs(output.e1_eta) < 1.442) & (abs(output.e2_eta) < 1.442)), "r"
        ] = "bb"
        output.loc[
            ((abs(output.e1_eta) > 1.566) ^ (abs(output.e2_eta) > 1.566)), "r"
        ] = "be"
        output.loc[
            ((abs(output.e1_eta) > 1.566) & (abs(output.e2_eta) > 1.566)), "r"
        ] = "ee"

        output["year"] = int(self.year)

#Aman edits
        for wgt in weights.df.columns:
            output[f"wgt_{wgt}"] = weights.get_weight(wgt)

#            if wgt == "pu_wgt_off":
#                output["pu_wgt"] = weights.get_weight(wgt)
#            if wgt != "nominal":
#                output[f"wgt_{wgt}"] = weights.get_weight(wgt)


        if is_mc and "dy" in dataset and self.applykFac:
            mass_bb = output[output["r"] == "bb"].dielectron_mass_gen.to_numpy()
            mass_be = output[output["r"] == "be"].dielectron_mass_gen.to_numpy()
            for key in output.columns:
                if "wgt" not in key[0]:
                    continue
                output.loc[
                    ((abs(output.e1_eta) < 1.442) & (abs(output.e2_eta) < 1.442)),
                    key[0],
                ] = (
                    output.loc[
                        ((abs(output.e1_eta) < 1.442) & (abs(output.e2_eta) < 1.442)),
                        key[0],
                    ]
                    * kFac(mass_bb, "bb", "el")
                ).values
                output.loc[
                    ((abs(output.e1_eta) > 1.566) ^ (abs(output.e2_eta) > 1.566)),
                    key[0],
                ] = (
                    output.loc[
                        ((abs(output.e1_eta) > 1.566) ^ (abs(output.e2_eta) > 1.566)),
                        key[0],
                    ]
                    * kFac(mass_be, "be", "el")
                ).values

        if is_mc and "dy" in dataset and self.applyNNPDFWeight:
            mass_bb = output[output["r"] == "bb"].dielectron_mass_gen.to_numpy()
            mass_be = output[output["r"] == "be"].dielectron_mass_gen.to_numpy()
            leadingPt_bb = output[output["r"] == "bb"].e1_pt_gen.to_numpy()
            leadingPt_be = output[output["r"] == "be"].e1_pt_gen.to_numpy()
            for key in output.columns:
                if "wgt" not in key[0]:
                    continue
                output.loc[
                    ((abs(output.e1_eta) < 1.442) & (abs(output.e2_eta) < 1.442)),
                    key[0],
                ] = (
                    output.loc[
                        ((abs(output.e1_eta) < 1.442) & (abs(output.e2_eta) < 1.442)),
                        key[0],
                    ]
                    * NNPDFWeight(
                        mass_bb, leadingPt_bb, "bb", "el", float(self.year), DY=True
                    )
                ).values
                output.loc[
                    ((abs(output.e1_eta) > 1.566) ^ (abs(output.e2_eta) > 1.566)),
                    key[0],
                ] = (
                    output.loc[
                        ((abs(output.e1_eta) > 1.566) ^ (abs(output.e2_eta) > 1.566)),
                        key[0],
                    ]
                    * NNPDFWeight(
                        mass_be, leadingPt_be, "be", "el", float(self.year), DY=True
                    )
                ).values
        if is_mc and "ttbar" in dataset and self.applyNNPDFWeight:
            mass_bb = output[output["r"] == "bb"].dielectron_mass_gen.to_numpy()
            mass_be = output[output["r"] == "be"].dielectron_mass_gen.to_numpy()
            leadingPt_bb = output[output["r"] == "bb"].e1_pt_gen.to_numpy()
            leadingPt_be = output[output["r"] == "be"].e1_pt_gen.to_numpy()
            
            for key in output.columns:
                if "wgt" not in key[0]:
                    continue
                output.loc[
                    ((abs(output.e1_eta) < 1.442) & (abs(output.e2_eta) < 1.442)),
                    key[0],
                ] = (
                    output.loc[
                        ((abs(output.e1_eta) < 1.442) & (abs(output.e2_eta) < 1.442)),
                        key[0],
                    ]
                    * NNPDFWeight(
                        mass_bb, leadingPt_bb, "bb", "el", float(self.year), DY=False
                    )
                ).values
                output.loc[
                    ((abs(output.e1_eta) > 1.566) ^ (abs(output.e2_eta) > 1.566)),
                    key[0],
                ] = (
                    output.loc[
                        ((abs(output.e1_eta) > 1.566) ^ (abs(output.e2_eta) > 1.566)),
                        key[0],
                    ]
                    * NNPDFWeight(
                        mass_be, leadingPt_be, "be", "el", float(self.year), DY=False
                    )
                ).values

        output = output.loc[output.event_selection, :]
        output = output.reindex(sorted(output.columns), axis=1)
        output = output[output.r.isin(self.regions)]
        output.columns = output.columns.droplevel("Variation")

        if self.timer:
            self.timer.add_checkpoint("Filled outputs")
            self.timer.summary()

        if self.apply_to_output is None:
            return output
        else:
            self.apply_to_output(output)
            return self.accumulator.identity()

    def jet_loop(
        self,
        variation,
        is_mc,
        df,
        dataset,
        mask,
        electrons,
        e1,
        e2,
        jets,
        jet_branches,
        weights,
        numevents,
        output,
    ):

        if not is_mc and variation != "nominal":
            return

        variables = pd.DataFrame(index=output.index)
        jet_branches_local = copy.copy(jet_branches)

        if is_mc:
            jets["pt_gen"] = jets.matched_gen.pt
            jets["eta_gen"] = jets.matched_gen.eta
            jets["phi_gen"] = jets.matched_gen.phi

            jet_branches_local += [
                "partonFlavour",
                "hadronFlavour",
                "pt_gen",
                "eta_gen",
                "phi_gen",
            ]
#            jets["pt_gen"] = jets.matched_gen.pt
#            jets["eta_gen"] = jets.matched_gen.eta
#            jets["phi_gen"] = jets.matched_gen.phi

        # Find jets that have selected muons within dR<0.4 from them
        matched_ele_pt = jets.matched_electrons.pt
        matched_ele_id = jets.matched_electrons[self.parameters["electron_id"]]
        matched_ele_pass = (
            (matched_ele_pt > self.parameters["electron_pt_cut"]) &
            matched_ele_id
        )
        clean = ~(ak.to_pandas(matched_ele_pass).astype(float).fillna(0.0)
                  .groupby(level=[0, 1]).sum().astype(bool))

        if self.timer:
             self.timer.add_checkpoint("Clean jets from matched electrons")

        # --- conversion from awkward to pandas --- #

        jets = jets[jet_branches_local]

        jets = ak.to_pandas(jets)

        if jets.index.nlevels == 3:
            # sometimes there are duplicates?
            jets = jets.loc[pd.IndexSlice[:, :, 0], :]
            jets.index = jets.index.droplevel("subsubentry")

        # ------------------------------------------------------------#
        # Apply jetID
        # ------------------------------------------------------------#
        # Sort jets by pT and reset their numbering in an event
        # jets = jets.sort_values(["entry", "pt"], ascending=[True, False])
        jets.index = pd.MultiIndex.from_arrays(
            [jets.index.get_level_values(0), jets.groupby(level=0).cumcount()],
            names=["entry", "subentry"],
        )

        jets = jets.dropna()
        jets = jets.loc[:, ~jets.columns.duplicated()]
 
        if self.do_btag:
            if is_mc:
                btagSF(jets, self.years, correction="shape", is_UL=True)
                btagSF(jets, self.years, correction="wp", is_UL=True)

                variables["wgt_nominal"] = (
                    jets.loc[jets.pre_selection == 1, "btag_sf_wp"]
                    .groupby("entry")
                    .prod()
                )
                variables["wgt_nominal"] = variables["wgt_nominal"].fillna(1.0)
                variables["wgt_nominal"] = variables[
                    "wgt_nominal"
                ] * weights.get_weight("nominal")
                variables["wgt_btag_up"] = (
                    jets.loc[jets.pre_selection == 1, "btag_sf_wp_up"]
                    .groupby("entry")
                    .prod()
                )
                variables["wgt_btag_up"] = variables["wgt_btag_up"].fillna(1.0)
                variables["wgt_btag_up"] = variables[
                    "wgt_btag_up"
                ] * weights.get_weight("nominal")
                variables["wgt_btag_down"] = (
                    jets.loc[jets.pre_selection == 1, "btag_sf_wp_down"]
                    .groupby("entry")
                    .prod()
                )
                variables["wgt_btag_down"] = variables["wgt_btag_down"].fillna(1.0)
                variables["wgt_btag_down"] = variables[
                    "wgt_btag_down"
                ] * weights.get_weight("nominal")


                ## further breakdown of btag systematics recommended by BTV POG

##bc up correlated
                variables["wgt_btag_bc_up_correlated"] = (
                    jets.loc[((jets.pre_selection == 1)&(jets.hadronFlavour>=4)), "btag_sf_wp_up_correlated"]
                    .groupby("entry")
                    .prod()
                )
                variables["wgt_btag_bc_up_correlated"] = variables["wgt_btag_bc_up_correlated"].fillna(1.0)

                variables["wgt_btag_bc_up_correlated"] = variables[
                    "wgt_btag_bc_up_correlated"
                ] * weights.get_weight("nominal")

##bc up uncorrelated
                variables["wgt_btag_bc_up_uncorrelated"] = (
                    jets.loc[((jets.pre_selection == 1)&(jets.hadronFlavour>=4)), "btag_sf_wp_up_uncorrelated"]
                    .groupby("entry")
                    .prod()
                )
                variables["wgt_btag_bc_up_uncorrelated"] = variables["wgt_btag_bc_up_uncorrelated"].fillna(1.0)

                variables["wgt_btag_bc_up_uncorrelated"] = variables[
                    "wgt_btag_bc_up_uncorrelated"
                ] * weights.get_weight("nominal")

##bc down correlated
                variables["wgt_btag_bc_down_correlated"] = (
                    jets.loc[((jets.pre_selection == 1)&(jets.hadronFlavour>=4)), "btag_sf_wp_down_correlated"]
                    .groupby("entry")
                    .prod()
                )
                variables["wgt_btag_bc_down_correlated"] = variables["wgt_btag_bc_down_correlated"].fillna(1.0)

                variables["wgt_btag_bc_down_correlated"] = variables[
                    "wgt_btag_bc_down_correlated"
                ] * weights.get_weight("nominal")

##bc down uncorrelated
                variables["wgt_btag_bc_down_uncorrelated"] = (
                    jets.loc[((jets.pre_selection == 1)&(jets.hadronFlavour>=4)), "btag_sf_wp_down_uncorrelated"]
                    .groupby("entry")
                    .prod()
                )
                variables["wgt_btag_bc_down_uncorrelated"] = variables["wgt_btag_bc_down_uncorrelated"].fillna(1.0)

                variables["wgt_btag_bc_down_uncorrelated"] = variables[
                    "wgt_btag_bc_down_uncorrelated"
                ] * weights.get_weight("nominal")

##light hadron flavour
##up correlated

                variables["wgt_btag_light_up_correlated"] = (
                    jets.loc[((jets.pre_selection == 1)&(jets.hadronFlavour<4)), "btag_sf_wp_up_correlated"]
                    .groupby("entry")
                    .prod()
                )

                variables["wgt_btag_light_up_correlated"] = variables["wgt_btag_light_up_correlated"].fillna(1.0)

                variables["wgt_btag_light_up_correlated"] = variables[
                    "wgt_btag_light_up_correlated"
                ] * weights.get_weight("nominal")

##light up uncorrelated
                variables["wgt_btag_light_up_uncorrelated"] = (
                    jets.loc[((jets.pre_selection == 1)&(jets.hadronFlavour<4)), "btag_sf_wp_up_uncorrelated"]
                    .groupby("entry")
                    .prod()
                )

                variables["wgt_btag_light_up_uncorrelated"] = variables["wgt_btag_light_up_uncorrelated"].fillna(1.0)

                variables["wgt_btag_light_up_uncorrelated"] = variables[
                    "wgt_btag_light_up_uncorrelated"
                ] * weights.get_weight("nominal")

##down correlated

                variables["wgt_btag_light_down_correlated"] = (
                    jets.loc[((jets.pre_selection == 1)&(jets.hadronFlavour<4)), "btag_sf_wp_down_correlated"]
                    .groupby("entry")
                    .prod()
                )

                variables["wgt_btag_light_down_correlated"] = variables["wgt_btag_light_down_correlated"].fillna(1.0)

                variables["wgt_btag_light_down_correlated"] = variables[
                    "wgt_btag_light_down_correlated"
                ] * weights.get_weight("nominal")

##light down uncorrelated
                variables["wgt_btag_light_down_uncorrelated"] = (
                    jets.loc[((jets.pre_selection == 1)&(jets.hadronFlavour<4)), "btag_sf_wp_down_uncorrelated"]
                    .groupby("entry")
                    .prod()
                )

                variables["wgt_btag_light_down_uncorrelated"] = variables["wgt_btag_light_down_uncorrelated"].fillna(1.0)

                variables["wgt_btag_light_down_uncorrelated"] = variables[
                    "wgt_btag_light_down_uncorrelated"
                ] * weights.get_weight("nominal")


###################################

                variables["wgt_btag_up_correlated"] = (
                    jets.loc[jets.pre_selection == 1, "btag_sf_wp_up_correlated"]
                    .groupby("entry")
                    .prod()
                )
                variables["wgt_btag_up_correlated"] = variables["wgt_btag_up_correlated"].fillna(1.0)
                variables["wgt_btag_up_correlated"] = variables[
                    "wgt_btag_up_correlated"
                ] * weights.get_weight("nominal")

                variables["wgt_btag_up_uncorrelated"] = (
                    jets.loc[jets.pre_selection == 1, "btag_sf_wp_up_uncorrelated"]
                    .groupby("entry")
                    .prod()
                )

                variables["wgt_btag_up_uncorrelated"] = variables["wgt_btag_up_uncorrelated"].fillna(1.0)
                variables["wgt_btag_up_uncorrelated"] = variables[
                    "wgt_btag_up_uncorrelated"
                ] * weights.get_weight("nominal")

                variables["wgt_btag_down_correlated"] = (
                    jets.loc[jets.pre_selection == 1, "btag_sf_wp_down_correlated"]
                    .groupby("entry")
                    .prod()
                )

                variables["wgt_btag_down_correlated"] = variables["wgt_btag_down_correlated"].fillna(1.0)
                variables["wgt_btag_down_correlated"] = variables[
                    "wgt_btag_down_correlated"
                ] * weights.get_weight("nominal")

                variables["wgt_btag_down_uncorrelated"] = (
                    jets.loc[jets.pre_selection == 1, "btag_sf_wp_down_uncorrelated"]
                    .groupby("entry")
                    .prod()
                )
                variables["wgt_btag_down_uncorrelated"] = variables["wgt_btag_down_uncorrelated"].fillna(1.0)
                variables["wgt_btag_down_uncorrelated"] = variables[
                    "wgt_btag_down_uncorrelated"
                ] * weights.get_weight("nominal")

            else:
                variables["wgt_nominal"] = 1.0
                variables["wgt_btag_up"] = 1.0
                variables["wgt_btag_down"] = 1.0

                variables["wgt_btag_bc_up_correlated"] = 1.0
                variables["wgt_btag_bc_up_uncorrelated"] = 1.0
                variables["wgt_btag_bc_down_correlated"] = 1.0
                variables["wgt_btag_bc_down_uncorrelated"] = 1.0

                variables["wgt_btag_light_up_correlated"] = 1.0
                variables["wgt_btag_light_up_uncorrelated"] = 1.0
                variables["wgt_btag_light_down_correlated"] = 1.0
                variables["wgt_btag_light_down_uncorrelated"] = 1.0

                variables["wgt_btag_up_correlated"] = 1.0
                variables["wgt_btag_up_uncorrelated"] = 1.0
                variables["wgt_btag_down_correlated"] = 1.0
                variables["wgt_btag_down_uncorrelated"] = 1.0

        else:
            if is_mc:
                variables["wgt_nominal"] = 1.0
                variables["wgt_nominal"] = variables[
                    "wgt_nominal"
                ] * weights.get_weight("nominal")

            else:
                variables["wgt_nominal"] = 1.0
      

        jets["clean"] = clean

#Aman edits
        jets["HEMVeto"] = 1
        jets.loc[
            (
                (jets.pt >= 20.0)
                & (jets.eta >= -3.0)
                & (jets.eta <= -1.3)
                & (jets.phi >= -1.57)
                & (jets.phi <= -0.87)
            ),
            "HEMVeto",
        ] = 0

        
        jets["selection"] = 0
        jets.loc[
            ((jets.pt > 20.0) & (abs(jets.eta) < 2.4) & (jets.jetId >= 2) & (jets.clean) & (jets.HEMVeto >= parameters["2018HEM_veto"][self.years])),
            "selection",
        ] = 1
 
        njets = jets.loc[:, "selection"].groupby("entry").sum() 
        variables["njets"] = njets 

        jets["bselection"] = 0
        jets.loc[
            (
                (jets.pt > 20.0)
                & (abs(jets.eta) < 2.4)
                & (jets.btagDeepFlavB > parameters["UL_btag_medium"][self.years])
                & (jets.jetId >= 2)
                & (jets.clean)
                & (jets.HEMVeto >= parameters["2018HEM_veto"][self.years])
            ),
            "bselection",
        ] = 1

#        nbjets = jets.loc[:, "bselection"].groupby("entry").sum()
#        variables["nbjets"] = nbjets

        bjets = jets.query("bselection==1")
        bjets["new_btight"] = 0
        bjets["sub_bmedium"] = 0

        bjets.loc[
           (bjets.btagDeepFlavB > parameters["UL_btag_tight"][self.years]),
           "new_btight",
         ] = 1

        bjets.loc[
           (bjets.btagDeepFlavB > parameters["UL_btag_medium"][self.years]),
           "sub_bmedium",
         ] = 1

        bjets = bjets.sort_values(["entry", "pt"], ascending=[True, False])
        bjet1 = bjets.groupby("entry").nth(0)
        bjet2 = bjets.groupby("entry").nth(1)

        bjet1 = bjet1[bjet1.new_btight == 1]

        bjets["tagged_jets"] = 0
        bjets.loc[
           (bjet1.index.values),
           "tagged_jets",
         ] = 1

        if (not bjet2.empty):
            common_idx = bjet1.index.intersection(bjet2.index)


            idx_diff = bjet2.index.difference(common_idx)

            bjet2 = bjet2.loc[common_idx]



            idx_diff = bjet2.index.difference(common_idx)

        nbjets= bjets.loc[:, "tagged_jets"].groupby("entry").sum()


        variables["nbjets"] = nbjets
        variables["nbjets"] = variables["nbjets"].fillna(0)

        #print("nbjets \n" , nbjets)
        #print(bjets[["tagged_jets", "btagDeepFlavB"]], "\n")


        bJets = [bjet1, bjet2]


        electrons = [e1, e2]
        fill_bjets(output, variables, bJets, electrons, flavor="el", is_mc=is_mc)

        jets = jets.sort_values(["entry", "pt"], ascending=[True, False])
        jet1 = jets.groupby("entry").nth(0)
        jet2 = jets.groupby("entry").nth(1)
        Jets = [jet1, jet2]
        fill_jets(output, variables, Jets, flavor="el",  is_mc=is_mc)
        if self.timer:
            self.timer.add_checkpoint("Filled jet variables")


        # --------------------------------------------------------------#
        # Fill outputs
        # --------------------------------------------------------------#

        # All variables are affected by jet pT because of jet selections:
        # a jet may or may not be selected depending on pT variation.

        for key, val in variables.items():
            output.loc[:, key] = val

        del df
        del electrons
        del jets
        del bjets
        del e1
        del e2

        return output

    def prepare_lookups(self):
        # Pile-up reweighting
        self.pu_lookups = pu_lookups(self.parameters)
        self.jec_factories, self.jec_factories_data = jec_factories(self.years)
        # --- Evaluator
        #self.extractor = extractor()

        # Z-pT reweigting (disabled)
        #zpt_filename = self.parameters["zpt_weights_file"]
        #self.extractor.add_weight_sets([f"* * {zpt_filename}"])
        #if "2016" in self.year:
        #    self.zpt_path = "zpt_weights/2016_value"
        #else:
        #    self.zpt_path = "zpt_weights/2017_value"

        # Calibration of event-by-event mass resolution
        #for mode in ["Data", "MC"]:
        #    label = f"res_calib_{mode}_{self.year}"
        #    path = self.parameters["res_calib_path"]
        #    file_path = f"{path}/{label}.root"
        #    self.extractor.add_weight_sets([f"{label} {label} {file_path}"])

        #self.extractor.finalize()
        #self.evaluator = self.extractor.make_evaluator()

        #self.evaluator[self.zpt_path]._axes = self.evaluator[self.zpt_path]._axes[0]
        return

    def postprocess(self, accumulator):
        return accumulator
