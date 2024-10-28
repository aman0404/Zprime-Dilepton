import sys

sys.path.append("copperhead/")

#import ROOT
import awkward
import awkward as ak
import numpy as np

# np.set_printoptions(threshold=sys.maxsize)
import pandas as pd
import coffea.processor as processor
from coffea.lumi_tools import LumiMask
from processNano.weights import Weights

# correction helpers included from copperhead
from copperhead.stage1.corrections.pu_reweight import pu_lookups, pu_evaluator

# from copperhead.stage1.corrections.lepton_sf import musf_lookup

from processNano.corrections.lepton_sf import musf_evaluator 
from processNano.corrections.lepton_sf_iso import musf_iso_evaluator
from processNano.corrections.lepton_sf_hlt import musf_hlt_evaluator

from processNano.corrections.jec import jec_factories, apply_jec
from copperhead.stage1.corrections.l1prefiring_weights import l1pf_weights

# from copperhead.stage1.corrections.lhe_weights import lhe_weights
# from copperhead.stage1.corrections.pdf_variations import add_pdf_variations

# high mass dilepton specific corrections
from processNano.corrections.kFac import kFac
from processNano.corrections.nnpdfWeight import NNPDFWeight

from processNano.jets import prepare_jets, fill_jets, fill_bjets, btagSF

#aman edits
from processNano.corrections.met_corr  import corrMet

import copy

from processNano.muons import find_dimuon, fill_muons
from processNano.utils import bbangle
from processNano.utils import angle
from processNano.utils import overlap_removal

from config.parameters import parameters, muon_branches, jet_branches
from config.parameters import ele_branches

#from config.jec_parameters import jec_parameters

##top pT reweighting
from processNano.corrections.topPtweights import topPtWeight

#ttbar SF
from processNano.corrections.ttbar_sf import ttbar_sf

class DimuonProcessor(processor.ProcessorABC):
    def __init__(self, **kwargs):
        self.samp_info = kwargs.pop("samp_info", None)
        do_timer = kwargs.pop("do_timer", False)
        self.pt_variations = kwargs.get("pt_variations", ["nominal"])
        self.apply_to_output = kwargs.pop("apply_to_output", None)

        self.years = self.samp_info.years

        if(self.years == '2016pre' or self.years == '2016post'):
           self.year = '2016'
        else:
           self.year = self.years
        self.parameters = {k: v.get(self.years, None) for k, v in parameters.items()}

        print("processing year ",self.year)
#        self.parameters = {k: v[self.year] for k, v in parameters.items()}
        
        # self.do_btag_syst = kwargs.pop("do_btag_syst", None)
        self.do_btag = True
        # if self.do_btag_syst:
        #    self.btag_systs = self.parameters["btag_systs"]
        # else:
        #    self.btag_systs = []

        if self.samp_info is None:
            print("Samples info missing!")
            return
        self.applykFac = False
        self.applyNNPDFWeight = False
        #self.do_musf = False
        self.do_musf = True

        self.applyTopPtWeight = True
        self.do_pu = True
        self.auto_pu = True
        #self.do_l1pw = False  # L1 prefiring weights
        self.do_l1pw = True  # L1 prefiring weights
        #jec_pars = {k: v[self.years] for k, v in jec_parameters.items()}
        self.do_jecunc = False  #default : True
        self.do_jecunc_up   = False
        self.do_jecunc_down = False

        self.do_jerunc = False
        self.do_jerunc_up = False
        self.do_jerunc_down = False

        self.applyttbarSF = True


#        for ptvar in self.pt_variations:
#            if ptvar in jec_pars["jec_variations"]:
#                self.do_jecunc = True
#            if ptvar in jec_pars["jer_variations"]:
#                self.do_jerunc = True

        # self.timer = Timer("global") if do_timer else None
        self.timer = None
        self._columns = self.parameters["proc_columns"]

        self.regions = ["bb", "be"]
        self.channels = ["mumu"]

        self.lumi_weights = self.samp_info.lumi_weights
        # if self.do_btag_syst:
        #    self.btag_systs = [
        #        "jes",
        #        "lf",
        #        "hfstats1",
        #        "hfstats2",
        #        "cferr1",
        #        "cferr2",
        #        "hf",
        #        "lfstats1",
        #        "lfstats2",
        #    ]
        # else:
        #    self.btag_systs = []

        self.prepare_lookups()

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
        #output["met"] = df.MET.pt
        output["met_phi"] = df.MET.phi



        # Separate dataframe to keep track on weights
        # and their systematic variations
        weights = Weights(output)

        # calculate generated mass from generated particles using the coffea genParticles
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
            output["dimuon_mass_gen"] = cut
            output["dimuon_pt_gen"] = cut
            output["dimuon_eta_gen"] = cut
            output["dimuon_phi_gen"] = cut
            genMother = genPart[cut][:, 0] + genPart[cut][:, 1]
            output.loc[
                output["dimuon_mass_gen"] == True, ["dimuon_mass_gen"]
            ] = genMother.mass
            output.loc[
                output["dimuon_pt_gen"] == True, ["dimuon_pt_gen"]
            ] = genMother.pt
            output.loc[
                output["dimuon_eta_gen"] == True, ["dimuon_eta_gen"]
            ] = genMother.eta
            output.loc[
                output["dimuon_phi_gen"] == True, ["dimuon_phi_gen"]
            ] = genMother.phi
            output.loc[output["dimuon_mass_gen"] == False, ["dimuon_mass_gen"]] = -999.0
            output.loc[output["dimuon_pt_gen"] == False, ["dimuon_pt_gen"]] = -999.0
            output.loc[output["dimuon_eta_gen"] == False, ["dimuon_eta_gen"]] = -999.0
            output.loc[output["dimuon_phi_gen"] == False, ["dimuon_phi_gen"]] = -999.0

        else:
            output["dimuon_mass_gen"] = -999.0
            output["dimuon_pt_gen"] = -999.0
            output["dimuon_eta_gen"] = -999.0
            output["dimuon_phi_gen"] = -999.0

        output["dimuon_mass_gen"] = output["dimuon_mass_gen"].astype(float)
        output["dimuon_pt_gen"] = output["dimuon_pt_gen"].astype(float)
        output["dimuon_eta_gen"] = output["dimuon_eta_gen"].astype(float)
        output["dimuon_phi_gen"] = output["dimuon_phi_gen"].astype(float)

        if is_mc:
            # For MC: Apply gen.weights, pileup weights, lumi weights,
            # L1 prefiring weights

            genPart = df.GenPart
            mask = np.ones(numevents, dtype=bool)
            genweight = df.genWeight
            weights.add_weight("genwgt", genweight)
            weights.add_weight("lumi", self.lumi_weights[dataset])

#            if self.do_musf:
#                muID, muIso, muTrig = musf_evaluator(
#                    self.musf_lookup, self.year, numevents, mu1, mu2
#                )
#                weights.add_weight("muID", muID, how="all")
#                weights.add_weight("muIso", muIso, how="all")
#                weights.add_weight("muTrig", muTrig, how="all")
#            else:
#                weights.add_weight("muID", how="dummy_all")
#                weights.add_weight("muIso", how="dummy_all")
#                weights.add_weight("muTrig", how="dummy_all")

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
                if "L1PreFiringWeight" in df.fields:
                    l1pfw = l1pf_weights(df)
                    weights.add_weight("l1prefiring_wgt", l1pfw, how="all")
                else:
                    weights.add_weight("l1prefiring_wgt", how="dummy_vars")

        else:
            # For Data: apply Lumi mask
            lumi_info = LumiMask(self.parameters["lumimask_UL_mu"])
            mask = lumi_info(df.run, df.luminosityBlock)
        # Apply HLT to both Data and MC

        hlt = ak.to_pandas(df.HLT[self.parameters["mu_hlt"]])
        hlt = hlt[self.parameters["mu_hlt"]].sum(axis=1)

        if self.timer:
            self.timer.add_checkpoint("Applied HLT and lumimask")

        # ------------------------------------------------------------#
        # Update muon kinematics with Rochester correction,
        # FSR recovery and GeoFit correction
        # Raw pT and eta are stored to be used in event selection
        # ------------------------------------------------------------#

        # ------------------------------------------------------------#
        # Prepare jets
        # ------------------------------------------------------------#
        prepare_jets(df, is_mc)
        

        # ------------------------------------------------------------#
        # Apply JEC, get JEC and JER variations
        # ------------------------------------------------------------#

        jets = df.Jet

        #print("before jec \n", jets.pt)
        #print("before jec raw \n", jets.pt_raw)

        # Save raw variables before computing any corrections
        df["Muon", "pt_raw"] = df.Muon.pt

        df["Muon", "eta_raw"] = df.Muon.eta
        df["Muon", "phi_raw"] = df.Muon.phi

        df["Muon", "tunepRelPt"] = df.Muon.tunepRelPt
       
        df["Muon", "tunePpt"] = df.Muon.tunepRelPt * df.Muon.pt

        df["Muon", "pt"] = df["Muon", "tunePpt"]
#aman edits
        #output["met"] = corrMet(df.MET, df.Muon)
        

        if is_mc:
            df["Muon", "pt_gen"] = df.Muon.matched_gen.pt
            df["Muon", "eta_gen"] = df.Muon.matched_gen.eta
            df["Muon", "phi_gen"] = df.Muon.matched_gen.phi
            df["Muon", "idx"] = df.Muon.genPartIdx

       
       
##Aman edits
        
        ele_branches_local = copy.copy(ele_branches)

        df["Electron", "pt_raw"] = df.Electron.pt
        df["Electron", "eta_raw"] = df.Electron.eta
        df["Electron", "phi_raw"] = df.Electron.phi

        electrons = ak.to_pandas(df.Electron[ele_branches_local])
        #print("----- electrons -----")
        #print(electrons)

        electrons.pt = electrons.pt_raw * (electrons.scEtOverPt + 1.0)
        electrons.eta = electrons.eta_raw + electrons.deltaEtaSC
        electrons = electrons.dropna()
        electrons = electrons.loc[:, ~electrons.columns.duplicated()]

        electrons["selection"] = 0  
#        electrons.loc[((electrons.pt > 10.)
#                & (abs(electrons.eta) < 2.5)
#                & (electrons[self.parameters["electron_id"]] >0)
#                & (abs(electrons.dxy) < self.parameters["electron_dxy"])
#                & (abs(electrons.dz) < self.parameters["electron_dz"])),
#                "selection",
#        ] = 1
#
#        nelectrons = electrons.loc[:, "selection"].groupby("entry").sum()


        # for ...
        if True:  # indent reserved for loop over muon pT variations
            # According to HIG-19-006, these variations have negligible
            # effect on significance, but it's better to have them
            # implemented in the future

            # --- conversion from awkward to pandas --- #
            muon_branches_local = copy.copy(muon_branches)
            if is_mc:
                muon_branches_local += [
                    "genPartFlav",
                    "genPartIdx",
                    "pt_gen",
                    "eta_gen",
                    "phi_gen",
                    "idx",
                ]

            
            muons = ak.to_pandas(df.Muon[muon_branches_local])
            #print("----- muons -------")
            if self.timer:
                self.timer.add_checkpoint("load muon data")

##Aman edits
            electrons["veto"] = 0
            electrons.loc[((electrons.pt > 10.)
                & (abs(electrons.eta) < 2.5)
                & (electrons[self.parameters["electron_id"]] ==1)
                & (abs(electrons.dxy) < self.parameters["electron_dxy"])
                & (abs(electrons.dz) < self.parameters["electron_dz"])),
                "veto",
            ] = 1

            muons = muons.dropna()
            muons = muons.loc[:, ~muons.columns.duplicated()]

#Aman edits
            met_raw  = ak.to_pandas(df.MET)

            output["met"] = corrMet(met_raw, muons)
             

            # --------------------------------------------------------#
            # Select muons that pass pT, eta, isolation cuts,
            # muon ID and quality flags
            # Select events with 2 OS muons, no electrons,
            # passing quality cuts and at least one good PV
            # --------------------------------------------------------#

            # Apply event quality flag
            output["r"] = None
            output["dataset"] = dataset
            output["year"] = int(self.year)
            #if dataset == "dyInclusive50":
            #    muons = muons[muons.genPartFlav == 15]
            flags = ak.to_pandas(df.Flag)
            flags = flags[self.parameters["event_flags"]].product(axis=1)
            muons["pass_flags"] = True
            if self.parameters["muon_flags"]:
                muons["pass_flags"] = muons[self.parameters["muon_flags"]].product(
                    axis=1
                )

            muons["overlap"] = (overlap_removal(muons, electrons))

            muons["overlap"].fillna(1., inplace=True)


            # Define baseline muon selection (applied to pandas DF!)
            muons["selection"] = (
                (muons.pt > self.parameters["muon_pt_cut"])
                #(muons.pt_raw > self.parameters["muon_pt_cut"])
                & (abs(muons.eta_raw) < self.parameters["muon_eta_cut"])
                & (muons.tkRelIso < self.parameters["muon_iso_cut"])
                & (muons[self.parameters["muon_id"]] > 0)
                & (abs(muons.dxy) < self.parameters["muon_dxy"])
                & (abs(muons.dz) < self.parameters["muon_dz"])
                & (
                    (muons.ptErr.values / muons.pt.values)
                    < self.parameters["muon_ptErr/pt"]
                )
#                & muons.pass_flags
            )
            #print("test", muons.pt)

            # Count muons
            nmuons = (
                muons[muons.selection]
                .reset_index()
                .groupby("entry")["subentry"]
                .nunique()
            )
            # Find opposite-sign muons
            sum_charge = muons.loc[muons.selection, "charge"].groupby("entry").sum()

            #print(" \n")
            #print("nmuons ", nmuons)
            #print("\n")
            #print("sum_charge ", sum_charge)


            # Find events with at least one good primary vertex
            good_pv = ak.to_pandas(df.PV).npvsGood > 0

            # Define baseline event selection

            output["two_muons"] = (nmuons == 2) | (nmuons > 2)
            output["two_muons"] = output["two_muons"].fillna(False)


            output["event_selection"] = (
                mask
                & (hlt > 0)
                & (flags > 0)
                & (nmuons == 2)
                & (abs(sum_charge) < nmuons)
                & good_pv

            )


            if self.timer:
                self.timer.add_checkpoint("Selected events and muons")

            # --------------------------------------------------------#
            # Initialize muon variables
            # --------------------------------------------------------#
            muons = muons.join(electrons["veto"])
            muons["veto"] = muons["veto"].fillna(0)
            # Find pT-leading and subleading muons


   
            muons = muons[muons.selection & (nmuons >= 2) & (abs(sum_charge) < nmuons) & (hlt > 0)  ]
            #muons = muons[muons.selection & (nmuons >= 2) & (abs(sum_charge) < nmuons) & (hlt > 0) & (muons.overlap) ]

            nelectrons = muons.loc[:, "veto"].groupby("entry").sum()


            if self.timer:
                self.timer.add_checkpoint("muon object selection")
            if muons.shape[0] == 0:
                output = output.reindex(sorted(output.columns), axis=1)
                output = output[output.r.isin(self.regions)]

                # return output
                if self.apply_to_output is None:
                    return output
                else:
                    self.apply_to_output(output)
                    return self.accumulator.identity()

            result = muons.groupby("entry").apply(find_dimuon, is_mc=is_mc)

            if is_mc:
                dimuon = pd.DataFrame(
                    result.to_list(), columns=["idx1", "idx2", "mass"]
                )
            else:
                dimuon = pd.DataFrame(
                    result.to_list(), columns=["idx1", "idx2", "mass"]
                )
            mu1 = muons.loc[dimuon.idx1.values, :]
            mu2 = muons.loc[dimuon.idx2.values, :]
            mu1.index = mu1.index.droplevel("subentry")
            mu2.index = mu2.index.droplevel("subentry")
            if self.timer:
                self.timer.add_checkpoint("dimuon pair selection")


            output["bbangle"] = bbangle(mu1, mu2)

            output["event_selection"] = ((output.event_selection) & (nelectrons==0) & (
            output.bbangle > self.parameters["3dangle"]
                ))

            if is_mc:
               if self.do_musf:
                   muID = musf_evaluator(
                       self.parameters, self.year, mu1, mu2
                   )
                   muISO = musf_iso_evaluator(
                       self.parameters, self.year, mu1, mu2
                   )
                   muHLT = musf_hlt_evaluator(
                       self.parameters, self.year, mu1, mu2
                   )
                   weights.add_weight("muID", muID, how="all")
                   weights.add_weight("muISO", muISO, how="all")
                   weights.add_weight("muHLT", muHLT, how="all")
                   #weights.add_weight("muTrig", muTrig, how="all")
               else:
                   weights.add_weight("muID", how="dummy_all")
                   weights.add_weight("muISO", how="dummy_all")
                   weights.add_weight("muHLT", how="dummy_all")
                   #print("values are ---- ", muID, muIso, muTrig)

            if self.timer:
                self.timer.add_checkpoint("back back angle calculation")

            # --------------------------------------------------------#
            # Select events with muons passing leading pT cut
            # and trigger matching
            # --------------------------------------------------------#

            # Events where there is at least one muon passing
            # leading muon pT cut

            # if self.timer:
            #    self.timer.add_checkpoint("Applied trigger matching")

            # --------------------------------------------------------#
            # Fill dimuon and muon variables
            # --------------------------------------------------------#
            fill_muons(self, output, mu1, mu2, is_mc, self.year, weights)

        # ------------------------------------------------------------#
        # Prepare jets
        # ------------------------------------------------------------#
        #prepare_jets(df, is_mc)

        # ------------------------------------------------------------#
        # Apply JEC, get JEC and JER variations
        # ------------------------------------------------------------#

#        jets = df.Jet
        self.do_jec = True #default : True

        # We only need to reapply JEC for 2018 data
        # (unless new versions of JEC are released)
        # if ("data" in dataset) and ("2018" in self.year):
        #    self.do_jec = False

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

        
      

        #jets.pt = jets.JES_jes.up.pt
        #jets.eta = jets.JES_jes.up.eta
        #jets.phi = jets.JES_jes.up.phi

        #print("jet pt \n", jets.JES_jes.up.pt)
        #print("jer up", jets.JER.up.pt/jets.pt_raw)
 
#        if self.do_jecunc:
#           jets["pt"] = jets.JES_jes.up.pt
#           jets["eta"] = jets.JES_jes.up.eta
#           jets["phi"] = jets.JES_jes.up.phi
#
#        if self.do_jerunc:
#           jets["pt"] = jets.JER.down.pt




#        print("jet pt \n", jets.pt)
 
        if self.timer:
            self.timer.add_checkpoint("Jet preparation & event weights")

        for v_name in self.pt_variations:
            output_updated = self.jet_loop(
                v_name,
                is_mc,
                df,
                dataset,
                mask,
                muons,
                mu1,
                mu2,
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

            # if is_mc:
            """
            do_zpt = ('dy' in dataset)
            if do_zpt:
                zpt_weight = np.ones(numevents, dtype=float)
                zpt_weight[two_muons] =\
                    self.evaluator[self.zpt_path](
                        output['dimuon_pt'][two_muons]
                    ).flatten()
                weights.add_weight('zpt_wgt', zpt_weight)
            """

        if self.timer:
            self.timer.add_checkpoint("Computed event weights")

        # ------------------------------------------------------------#
        # Fill outputs
        # ------------------------------------------------------------#

        output.loc[
            ((abs(output.mu1_eta) < 1.2) & (abs(output.mu2_eta) < 1.2)), "r"
        ] = "bb"
        output.loc[
            ((abs(output.mu1_eta) > 1.2) | (abs(output.mu2_eta) > 1.2)), "r"
        ] = "be"


        output["year"] = int(self.year)
#Aman edits
        for wgt in weights.df.columns:
            output[f"wgt_{wgt}"] = weights.get_weight(wgt)

        if is_mc and "dy" in dataset and self.applykFac:
            mass_bb = output[output["r"] == "bb"].dimuon_mass_gen.to_numpy()
            mass_be = output[output["r"] == "be"].dimuon_mass_gen.to_numpy()
            for key in output.columns:
                if "wgt" not in key[0]:
                    continue
                output.loc[
                    ((abs(output.mu1_eta) < 1.2) & (abs(output.mu2_eta) < 1.2)),
                    key[0],
                ] = (
                    output.loc[
                        ((abs(output.mu1_eta) < 1.2) & (abs(output.mu2_eta) < 1.2)),
                        key[0],
                    ]
                    * kFac(mass_bb, "bb", "mu")
                ).values
                output.loc[
                    ((abs(output.mu1_eta) > 1.2) | (abs(output.mu2_eta) > 1.2)),
                    key[0],
                ] = (
                    output.loc[
                        ((abs(output.mu1_eta) > 1.2) | (abs(output.mu2_eta) > 1.2)),
                        key[0],
                    ]
                    * kFac(mass_be, "be", "mu")
                ).values

        if is_mc and "dy" in dataset and self.applyNNPDFWeight:
            mass_bb = output[output["r"] == "bb"].dimuon_mass_gen.to_numpy()
            mass_be = output[output["r"] == "be"].dimuon_mass_gen.to_numpy()
            leadingPt_bb = output[output["r"] == "bb"].mu1_pt_gen.to_numpy()
            leadingPt_be = output[output["r"] == "be"].mu1_pt_gen.to_numpy()
            for key in output.columns:
                if "wgt" not in key[0]:
                    continue
                output.loc[
                    ((abs(output.mu1_eta) < 1.2) & (abs(output.mu2_eta) < 1.2)),
                    key[0],
                ] = (
                    output.loc[
                        ((abs(output.mu1_eta) < 1.2) & (abs(output.mu2_eta) < 1.2)),
                        key[0],
                    ]
                    * NNPDFWeight(
                        mass_bb, leadingPt_bb, "bb", "mu", float(self.year), DY=True
                    )
                ).values
                output.loc[
                    ((abs(output.mu1_eta) > 1.2) | (abs(output.mu2_eta) > 1.2)),
                    key[0],
                ] = (
                    output.loc[
                        ((abs(output.mu1_eta) > 1.2) | (abs(output.mu2_eta) > 1.2)),
                        key[0],
                    ]
                    * NNPDFWeight(
                        mass_be, leadingPt_be, "be", "mu", float(self.year), DY=True
                    )
                ).values
        if is_mc and "ttbar" in dataset and self.applyNNPDFWeight:
            mass_bb = output[output["r"] == "bb"].dimuon_mass_gen.to_numpy()
            mass_be = output[output["r"] == "be"].dimuon_mass_gen.to_numpy()
            leadingPt_bb = output[output["r"] == "bb"].mu1_pt_gen.to_numpy()
            leadingPt_be = output[output["r"] == "be"].mu1_pt_gen.to_numpy()
            for key in output.columns:
                if "wgt" not in key[0]:
                    continue
                output.loc[
                    ((abs(output.mu1_eta) < 1.2) & (abs(output.mu2_eta) < 1.2)),
                    key[0],
                ] = (
                    output.loc[
                        ((abs(output.mu1_eta) < 1.2) & (abs(output.mu2_eta) < 1.2)),
                        key[0],
                    ]
                    * NNPDFWeight(
                        mass_bb, leadingPt_bb, "bb", "mu", float(self.year), DY=False
                    )
                ).values
                output.loc[
                    ((abs(output.mu1_eta) > 1.2) | (abs(output.mu2_eta) > 1.2)),
                    key[0],
                ] = (
                    output.loc[
                        ((abs(output.mu1_eta) > 1.2) | (abs(output.mu2_eta) > 1.2)),
                        key[0],
                    ]
                    * NNPDFWeight(
                        mass_be, leadingPt_be, "be", "mu", float(self.year), DY=False
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
        muons,
        mu1,
        mu2,
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

#        print("jet pt \n", jets.pt)
#        if self.do_jecunc and self.do_jecunc_up:
#           jets["pt"] = jets.JES_jes.up.pt
#           jets["eta"] = jets.JES_jes.up.eta
#           jets["phi"] = jets.JES_jes.up.phi
#
#        if self.do_jecunc and self.do_jecunc_down:
#           jets["pt"] = jets.JES_jes.down.pt
#           jets["eta"] = jets.JES_jes.down.eta
#           jets["phi"] = jets.JES_jes.down.phi
#
        if self.do_jerunc and self.do_jerunc_up:
           jets["pt"] = jets.JER.up.pt
           jets["eta"] = jets.JER.up.eta
           jets["phi"] = jets.JER.up.phi
#
#
#        if self.do_jerunc and self.do_jerunc_down:
#           jets["pt"] = jets.JER.down.pt
#           jets["eta"] = jets.JER.down.eta
#           jets["phi"] = jets.JER.down.phi



        if variation == "nominal":
           if self.do_jec:
               jet_branches_local += ["pt_jec", "mass_jec"]
           if is_mc and self.do_jerunc:
               jet_branches_local += ["pt_orig", "mass_orig"]

        # Find jets that have selected muons within dR<0.4 from them
        matched_mu_pt = jets.matched_muons.pt
        matched_mu_iso = jets.matched_muons.pfRelIso04_all

        matched_mu_id = jets.matched_muons[self.parameters["muon_id"]]

        matched_mu_pass = (
            (matched_mu_pt > self.parameters["muon_pt_cut"])
            & (matched_mu_iso < self.parameters["muon_iso_cut"])
            & matched_mu_id
        )



        clean = ~(
            ak.to_pandas(matched_mu_pass)
            .astype(float)
            .fillna(0.0)
            .groupby(level=[0, 1])
            .sum()
            .astype(bool)
        )

        if self.timer:
            self.timer.add_checkpoint("Clean jets from matched muons")

        # Select particular JEC variation
     
        #if "_up" in variation:
        #   unc_name = "JES_" + variation.replace("_up", "")

        #   if unc_name not in jets.fields:
        #       return
        #   jets = jets[unc_name]["up"][jet_branches_local]
        #elif "_down" in variation:
        #   unc_name = "JES_" + variation.replace("_down", "")
        #   if unc_name not in jets.fields:
        #       return
        #   jets = jets[unc_name]["down"][jet_branches_local]
        #else:
        #   jets = jets[jet_branches_local]

        jets = jets[jet_branches_local]

        # --- conversion from awkward to pandas --- #
        jets = ak.to_pandas(jets)

        #print(jets[["pt", "eta"]])

        if jets.index.nlevels == 3:
            # sometimes there are duplicates?
            jets = jets.loc[pd.IndexSlice[:, :, 0], :]
            jets.index = jets.index.droplevel("subsubentry")

        if variation == "nominal":
           #Update pt and mass if JEC was applied
           if self.do_jec:
               jets["pt"] = jets["pt_jec"]
               jets["mass"] = jets["mass_jec"]

        # We use JER corrections only for systematics, so we shouldn't
        # update the kinematics. Use original values,
        # unless JEC were applied.
        if is_mc and self.do_jerunc and not self.do_jec:
           jets["pt"] = jets["pt_orig"]
           jets["mass"] = jets["mass_orig"]

        #print("jet pt \n", jets.pt)
        # ------------------------------------------------------------#
        # Apply jetID
        # ------------------------------------------------------------#
        # Sort jets by pT and reset their numbering in an event
        # jets = jets.sort_values(["entry", "pt"], ascending=[True, False])
        jets.index = pd.MultiIndex.from_arrays(
            [jets.index.get_level_values(0), jets.groupby(level=0).cumcount()],
            names=["entry", "subentry"],
        )
        # Select two jets with highest pT
        # if is_mc:
        #    variables["btag_sf_shape"] = (
        #        jets.loc[jets.pre_selection == 1, "btag_sf_shape"]
        #        .groupby("entry")
        #        .prod()
        #    )
        #    variables["btag_sf_shape"] = variables["btag_sf_shape"].fillna(1.0)

        if self.do_btag:
            if is_mc:
                #btagSF(jets, self.years, correction="shape", is_UL=True)
                btagSF(jets, self.years, correction="wp", is_UL=True)
                jets = jets.dropna()

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


##############################
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


                for s in ["_up", "_down"]:

                    variables["wgt_recowgt" + s] = (
                        jets.loc[jets.pre_selection == 1, "btag_sf_wp"]
                        .groupby("entry")
                        .prod()
                    )
                    variables["wgt_recowgt" + s] = variables["wgt_recowgt" + s].fillna(
                        1.0
                    )
                    variables["wgt_recowgt" + s] = variables[
                        "wgt_recowgt" + s
                    ] * weights.get_weight("recowgt" + s)
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
                variables["wgt_recowgt_up"] = 1.0
                variables["wgt_recowgt_down"] = 1.0
        else:
            if is_mc:
                variables["wgt_nominal"] = 1.0
                variables["wgt_nominal"] = variables[
                    "wgt_nominal"
                ] * weights.get_weight("nominal")

                for s in ["_up", "_down"]:

                    variables["wgt_recowgt" + s] = 1.0
                    variables["wgt_recowgt" + s] = variables[
                        "wgt_recowgt" + s
                    ] * weights.get_weight("recowgt" + s)
            else:
                variables["wgt_nominal"] = 1.0
                variables["wgt_recowgt_up"] = 1.0
                variables["wgt_recowgt_down"] = 1.0


        jets["clean"] = clean

#        is_overlapping = ( 
#             (overlap_removal(muons, jets) > 0.4)
#        )
#        
#        dr_clean = (
#            ak.to_pandas(is_overlapping)
#        )


#        jets["overlap"] = dr_clean

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
#        jets.loc[
#            ((jets.pt > 20.0) & (abs(jets.eta) < 2.4) & (jets.jetId >= 2) & (jets.clean) & (jets.HEMVeto >= parameters["2018HEM_veto"][self.years])
#            
#            ),
#            "selection",
#        ] = 1

        jets.loc[
            ((jets.pt > 20.0) & (abs(jets.eta) < 2.4) & (jets.jetId >= 2) & (jets.clean) & (jets.HEMVeto >= parameters["2018HEM_veto"][self.years])

            ),
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

        #print(parameters["UL_btag_medium"][self.year])
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

        muons = [mu1, mu2]
        fill_bjets(output, variables, bJets, muons, is_mc=is_mc)

        variables["dataset"] =  dataset

        output["regions"] = None

        output.loc[
            ((abs(output.mu1_eta) < 1.2) & (abs(output.mu2_eta) < 1.2)), "regions"
        ] = "bb"
        output.loc[
            ((abs(output.mu1_eta) > 1.2) | (abs(output.mu2_eta) > 1.2)), "regions"
        ] = "be"

        variables["regions"] = output["regions"]        
        variables["year"] =  output["year"]


        if self.applyttbarSF:
            variables["ttbar_sfs"] = variables.apply(ttbar_sf, axis = 1)
            weights.add_weight("ttbar_sf", variables.ttbar_sfs)
            #print("sfs ",variables["ttbar_sfs"])

#        vec_mu1 = ROOT.TVector(mu1)
#        vec_b1 =  ROOT.TVector(bjet1)
#        output["lb_angle"] = angle(mu1, bjet1)

        jets = jets.sort_values(["entry", "pt"], ascending=[True, False])
        jet1 = jets.groupby("entry").nth(0)
        jet2 = jets.groupby("entry").nth(1)
        Jets = [jet1, jet2]
        fill_jets(output, variables, Jets, is_mc=is_mc)
        if self.timer:
            self.timer.add_checkpoint("Filled jet variables")

        # ------------------------------------------------------------#
        # Calculate btag SF
        # ------------------------------------------------------------#
        # --- Btag weights --- #
        # if is_mc:
        # bjet_sel_mask = output.event_selection

        # btag_wgt, btag_syst = btag_weights(
        #    self, self.btag_lookup, self.btag_systs, jets, weights, bjet_sel_mask
        # )
        # weights.add_weight("btag_wgt", btag_wgt)

        # --- Btag weights variations --- #
        # for name, bs in btag_syst.items():
        #    weights.add_weight(f"btag_wgt_{name}", bs, how="only_vars")

        # if self.timer:
        #    self.timer.add_checkpoint(
        #        "Applied B-tag weights"
        #    )

        # --------------------------------------------------------------#
        # Fill outputs
        # --------------------------------------------------------------#
        # variables.update({"wgt_nominal": weights.get_weight("nominal")})
        # All variables are affected by jet pT because of jet selections:
        # a jet may or may not be selected depending on pT variation.

        for key, val in variables.items():
            output.loc[:, key] = val

        del df
        del muons
        del jets
        del bjets
        del mu1
        del mu2
        return output



    def prepare_lookups(self):
        self.jec_factories, self.jec_factories_data = jec_factories(self.years)
        # Muon scale factors
        #self.musf_lookup = musf_lookup(self.parameters)
        # Pile-up reweighting
        self.pu_lookups = pu_lookups(self.parameters)
        # Btag weights
        # self.btag_lookup = BTagScaleFactor(
        #        "data/b-tagging/DeepCSV_102XSF_WP_V1.csv", "medium"
        #    )
        # self.btag_lookup = BTagScaleFactor(
        #    self.parameters["btag_sf_csv"],
        #    BTagScaleFactor.RESHAPE,
        #    "iterativefit,iterativefit,iterativefit",
        # )
        # self.btag_lookup = btagSF("2018", jets.hadronFlavour, jets.eta, jets.pt, jets.btagDeepFlavB)

        # --- Evaluator
        # self.extractor = extractor()
        # PU ID weights
        # puid_filename = self.parameters["puid_sf_file"]
        # self.extractor.add_weight_sets([f"* * {puid_filename}"])

        # self.extractor.finalize()
        # self.evaluator = self.extractor.make_evaluator()

        return

    @property
    def accumulator(self):
        return processor.defaultdict_accumulator(int)

    @property
    def muoncolumns(self):
        return muon_branches

    @property
    def jetcolumns(self):
        return jet_branches

    def postprocess(self, accumulator):
        return accumulator
