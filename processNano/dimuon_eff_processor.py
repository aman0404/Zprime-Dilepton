import sys

sys.path.append("copperhead/")

import awkward as ak
import numpy as np

# np.set_printoptions(threshold=sys.maxsize)
import pandas as pd
import coffea.processor as processor
from coffea.lookup_tools import extractor
from coffea.lumi_tools import LumiMask

from processNano.timer import Timer
from processNano.weights import Weights

from copperhead.stage1.corrections.pu_reweight import pu_lookups, pu_evaluator
from copperhead.stage1.corrections.lepton_sf import musf_lookup
from copperhead.stage1.corrections.fsr_recovery import fsr_recovery
from copperhead.stage1.corrections.jec import jec_factories
from copperhead.stage1.corrections.l1prefiring_weights import l1pf_weights
from processNano.jets import fill_jets
import copy

# from python.jets import jet_id, jet_puid, gen_jet_pair_mass
from processNano.muons import find_dimuon
from processNano.utils import p4_sum

from config.parameters import parameters, muon_branches, jet_branches


class DimuonEffProcessor(processor.ProcessorABC):
    def __init__(self, **kwargs):
        self.samp_info = kwargs.pop("samp_info", None)
        do_timer = kwargs.pop("do_timer", True)
        self.apply_to_output = kwargs.pop("apply_to_output", None)
        self.do_btag_syst = kwargs.pop("do_btag_syst", None)
        self.pt_variations = kwargs.pop("pt_variations", ["nominal"])

        if self.samp_info is None:
            print("Samples info missing!")
            return

        self._accumulator = processor.defaultdict_accumulator(int)

        self.do_pu = False
        self.auto_pu = False
        self.year = self.samp_info.year
        self.do_roccor = False
        self.do_fsr = False
        self.do_geofit = False
        self.do_l1pw = False  # L1 prefiring weights
        self.do_jecunc = False
        self.do_jerunc = False
        self.parameters = {k: v[self.year] for k, v in parameters.items()}

        self.timer = Timer("global") if do_timer else None

        self._columns = self.parameters["proc_columns"]

        self.regions = ["bb", "be"]
        self.channels = ["mumu"]

        self.lumi_weights = self.samp_info.lumi_weights
        if self.do_btag_syst:
            self.btag_systs = [
                "jes",
                "lf",
                "hfstats1",
                "hfstats2",
                "cferr1",
                "cferr2",
                "hf",
                "lfstats1",
                "lfstats2",
            ]
        else:
            self.btag_systs = []

        #        self.vars_to_save = set([v.name for v in variables])
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

        is_mc = "data" not in dataset

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
        if not is_mc:
            print("cannot calculate acceptance and efficiency with data")
            return
        # Separate dataframe to keep track on weights
        # and their systematic variations
        weights = Weights(output)

        if is_mc:
            # For MC: Apply gen.weights, pileup weights, lumi weights,
            # L1 prefiring weights
            mask = np.ones(numevents, dtype=bool)
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
            if self.do_l1pw:
                if self.parameters["do_l1prefiring_wgts"]:
                    if "L1PreFiringWeight" in df.fields:
                        l1pfw = l1pf_weights(df)
                        weights.add_weight("l1prefiring_wgt", l1pfw, how="all")
                    else:
                        weights.add_weight("l1prefiring_wgt", how="dummy_vars")

        else:
            # For Data: apply Lumi mask
            lumi_info = LumiMask(self.parameters["lumimask_Pre-UL_mu"])
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

        # Save raw variables before computing any corrections
        df["Muon", "pt_raw"] = df.Muon.pt
        df["Muon", "eta_raw"] = df.Muon.eta
        df["Muon", "phi_raw"] = df.Muon.phi
        df["Muon", "pt_gen"] = df.Muon.matched_gen.pt
        df["Muon", "eta_gen"] = df.Muon.matched_gen.eta
        df["Muon", "phi_gen"] = df.Muon.matched_gen.phi
        if True:  # indent reserved for loop over muon pT variations
            # According to HIG-19-006, these variations have negligible
            # effect on significance, but it's better to have them
            # implemented in the future

            # FSR recovery
            if self.do_fsr:
                has_fsr = fsr_recovery(df)
                df["Muon", "pt"] = df.Muon.pt_fsr
                df["Muon", "eta"] = df.Muon.eta_fsr
                df["Muon", "phi"] = df.Muon.phi_fsr
                df["Muon", "pfRelIso04_all"] = df.Muon.iso_fsr

                if self.timer:
                    self.timer.add_checkpoint("FSR recovery")

            # if FSR was applied, 'pt_fsr' will be corrected pt
            # if FSR wasn't applied, just copy 'pt' to 'pt_fsr'
            df["Muon", "pt_fsr"] = df.Muon.pt

            # --- conversion from awkward to pandas --- #
            muon_branches_local = copy.copy(muon_branches)
            muon_branches_local += ["genPartIdx", "pt_gen", "eta_gen", "phi_gen"]
            gen_branches = [
                "pt",
                "eta",
                "phi",
                "mass",
                "statusFlags",
                "status",
                "pdgId",
            ]
            genPart = ak.to_pandas(df.GenPart[gen_branches])
            # print("genPart shape")
            # print(genPart.shape)
            df["Jet", "pt_reco"] = df.Jet.pt
            df["Jet", "eta_reco"] = df.Jet.eta
            # df["Jet", "flavor_reco"]=df.Jet.hadronFlavour
            jet_branches_local = copy.copy(jet_branches)
            jet_branches_local += [
                "partonFlavour",
                "hadronFlavour",
                "genJetIdx",
                "pt_reco",
                "eta_reco",
            ]
            jets = ak.to_pandas(df.Jet[jet_branches_local])
            # print(jets.hadronFlavour)
            # jets["hadronFlavour"] = jets["hadronFlavour"].astype(int)
            # jets = jets[(jets["hadronFlavour"]==0)|(jets["hadronFlavour"]==4)|(jets["hadronFlavour"]==5)]
            jets["flavor_reco"] = jets["hadronFlavour"]
            # print(jets[].flavor_reco)
            # jets["pt_reco"] = jets.pt
            # jets["eta_reco"] = jets.eta
            # jets["flavor_reco"] = jets.hadronFlavour
            genJets = ak.to_pandas(
                df.GenJet[["pt", "eta", "phi", "partonFlavour", "hadronFlavour"]]
            )
            muons = ak.to_pandas(df.Muon[muon_branches_local])
            if self.timer:
                self.timer.add_checkpoint("load muon data")
            muons = muons.dropna()
            muons = muons.loc[:, ~muons.columns.duplicated()]
            # --------------------------------------------------------#
            # Select muons that pass pT, eta, isolation cuts,
            # muon ID and quality flags
            # Select events with 2 OS muons, no electrons,
            # passing quality cuts and at least one good PV
            # --------------------------------------------------------#

            # Apply event quality flag
            flags = ak.to_pandas(df.Flag)
            flags = flags[self.parameters["event_flags"]].product(axis=1)
            muons["pass_flags"] = True
            if self.parameters["muon_flags"]:
                muons["pass_flags"] = muons[self.parameters["muon_flags"]].product(
                    axis=1
                )

            # Define baseline muon selection (applied to pandas DF!)
            muons["ID"] = (
                (muons.tkRelIso < self.parameters["muon_iso_cut"])
                & (muons[self.parameters["muon_id"]] > 0)
                & (muons.dxy < self.parameters["muon_dxy"])
                & (
                    (muons.ptErr.values / muons.pt.values)
                    < self.parameters["muon_ptErr/pt"]
                )
            )

            # Find events with at least one good primary vertex
            good_pv = ak.to_pandas(df.PV).npvsGood > 0

            # Define baseline event selection

            if self.timer:
                self.timer.add_checkpoint("Selected events and muons")

            # --------------------------------------------------------#
            # Initialize muon variables
            # --------------------------------------------------------#

            # Find pT-leading and subleading muons

            # if self.timer:
            #    self.timer.add_checkpoint("back back angle calculation")

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

        # Prepare jets
        # ------------------------------------------------------------#

        # ------------------------------------------------------------#
        # Apply JEC, get JEC and JER variations
        # ------------------------------------------------------------#

        if self.timer:
            self.timer.add_checkpoint("Computed event weights")

        # ------------------------------------------------------------#
        # Fill outputs
        # ------------------------------------------------------------#

        for wgt in weights.df.columns:

            if wgt != "nominal":
                continue
            wgt_list = weights.get_weight(wgt)
        wgt = pd.DataFrame(wgt_list, columns=["wgt_nominal"])
        wgt.index.names = ["entry"]

        jets.set_index("genJetIdx", append=True, inplace=True)
        jets.reset_index("subentry", inplace=True)
        jets.drop("subentry", axis=1, inplace=True)
        jets.index.names = ["entry", "subentry"]
        jets.loc[
            jets.btagDeepFlavB > parameters["UL_btag_medium"][self.year], "btag"
        ] = True
        jets.loc[jets.jetId >= 2, "Jet_ID"] = True
        jets["Jet_match"] = True
        genJets = genJets.merge(
            jets[["Jet_match", "Jet_ID", "btag", "pt_reco", "eta_reco", "flavor_reco"]],
            on=["entry", "subentry"],
            how="left",
        )
        genJets.fillna(False, inplace=True)
        genJets.rename(
            columns={
                "pt": "Jet_pt",
                "eta": "Jet_eta",
                "phi": "Jet_phi",
                "pt_reco": "Jet_pt_reco",
                "eta_reco": "Jet_eta_reco",
            },
            inplace=True,
        )

        nJets = genJets.reset_index().groupby("entry")["subentry"].nunique()
        jets = nJets.to_numpy()

        # print(len(jets))
        # print(nJets.head())
        # print(jets)
        # print("0 jet events")
        # print(len(jets[jets==0]))
        # print("1 jet events")
        # print(len(jets[jets==1]))
        # print("2 jet events")
        # print(len(jets[jets>=2]))
        nJets_acc = (
            genJets[(abs(genJets.Jet_eta) < 2.4) & (genJets.Jet_pt > 30)]
            .reset_index()
            .groupby("entry")["subentry"]
            .nunique()
        )
        nJets_pt = (
            genJets[genJets.Jet_pt > 30]
            .reset_index()
            .groupby("entry")["subentry"]
            .nunique()
        )
        nJets_match = (
            genJets[(genJets.Jet_match) & (genJets.Jet_pt > 30)]
            .reset_index()
            .groupby("entry")["subentry"]
            .nunique()
        )
        nJets_ID = (
            genJets[(genJets.Jet_ID) & (genJets.Jet_match) & (genJets.Jet_pt > 30)]
            .reset_index()
            .groupby("entry")["subentry"]
            .nunique()
        )
        nJets_btag = (
            genJets[
                (genJets.btag)
                & (genJets.Jet_ID)
                & (genJets.Jet_match)
                & (genJets.Jet_pt > 30)
            ]
            .reset_index()
            .groupby("entry")["subentry"]
            .nunique()
        )
        nJets = nJets.to_frame("nJets")
        nJets_acc = nJets_acc.to_frame("nJets_accepted")
        nJets_pt = nJets_pt.to_frame("nJets_pt_pass")
        nJets_match = nJets_match.to_frame("nJets_reco")
        nJets_ID = nJets_ID.to_frame("nJets_ID")
        nJets_btag = nJets_btag.to_frame("nJets_btag")

        muons.set_index("genPartIdx", append=True, inplace=True)
        muons.reset_index("subentry", inplace=True)
        muons.drop("subentry", axis=1, inplace=True)
        muons.index.names = ["entry", "subentry"]
        muons["match"] = True
        hlt = hlt.to_frame("hlt")

        good_pv = good_pv.to_frame("gpv")
        genPart = genPart.merge(
            muons[["match", "pt_raw", "ID"]], on=["entry", "subentry"], how="left"
        )
        genPart.pt_raw.fillna(-999.0, inplace=True)
        genPart.fillna(False, inplace=True)
        genPart = genPart[
            (genPart.status == 1)
            & (abs(genPart.pdgId) == 13)
            #& (genPart.statusFlags == 8449)
        ]
        genPart.loc[genPart["pdgId"] == -13, "charge"] = -1
        genPart.loc[genPart["pdgId"] == 13, "charge"] = 1
        sum_sign = genPart.loc[:, "charge"].groupby("entry").sum()
        nGen = genPart.reset_index().groupby("entry")["subentry"].nunique()
        # print(nGen.head())
        genPart = genPart[
            (genPart["status"] == 1) & (nGen >= 2) & (abs(sum_sign) < nGen)
        ]
        # print("check if 2 particles in genpart")
        # print(genPart.head())
        print(genPart[["ID", "status"]])
        result = genPart.groupby("entry").apply(find_dimuon, is_mc=False)
        dimuon = pd.DataFrame(result.to_list(), columns=["idx1", "idx2", "dimuon_mass"])
        mu1 = genPart.loc[dimuon.idx1.values, :]
        mu2 = genPart.loc[dimuon.idx2.values, :]
        mu1.index = mu1.index.droplevel("subentry")
        mu2.index = mu2.index.droplevel("subentry")
        mm = p4_sum(mu1, mu2, is_mc=False)
        mm.rename(columns={"mass": "dimuon_mass"}, inplace=True)
        pt_pass = (
            genPart[genPart["pt"] > 53]
            .reset_index()
            .groupby("entry")["subentry"]
            .nunique()
            >= 2
        )
        pt_pass = pt_pass.to_frame("pt_pass")
        acc = (
            genPart[(abs(genPart["eta"]) < 2.4) & (genPart["pt"] > 53)]
            .reset_index()
            .groupby("entry")["subentry"]
            .nunique()
            >= 2
        )
        acc = acc.to_frame("accepted")
        reco = (
            genPart[genPart["match"]]
            .reset_index()
            .groupby("entry")["subentry"]
            .nunique()
            >= 2
        )
        reco = reco.to_frame("reco")
        ID = (
            genPart[genPart["ID"]].reset_index().groupby("entry")["subentry"].nunique()
            >= 2
        )
        ID = ID.to_frame("ID_pass")

        genPart.drop(columns=["statusFlags", "status", "pdgId"], inplace=True)
        genPart = pd.concat(
            [
                genPart,
                genJets[
                    [
                        "Jet_match",
                        "Jet_ID",
                        "btag",
                        "Jet_pt",
                        "Jet_eta",
                        "Jet_phi",
                        "partonFlavour",
                        "hadronFlavour",
                        "flavor_reco",
                        "Jet_pt_reco",
                        "Jet_eta_reco",
                    ]
                ],
            ],
            levels=0,
        ).sort_index()
        genPart[["Jet_match", "Jet_ID", "btag", "match", "ID"]] = genPart[
            ["Jet_match", "Jet_ID", "btag", "match", "ID"]
        ].fillna(False)
        genPart[["Jet_pt", "Jet_eta", "Jet_phi", "pt", "eta", "phi", "mass"]] = genPart[
            ["Jet_pt", "Jet_eta", "Jet_phi", "pt", "eta", "phi", "mass"]
        ].fillna(-999.0)
        # print("check genPart and genJets heads")
        # print(genPart.head)
        # print(nJets.head)
        genPart = (
            genPart.reset_index("subentry")
            .merge(nJets["nJets"], on=["entry"], how="left")
            .set_index("subentry", append=True)
        )
        # print("check merge")
        # print(genPart.nJets)
        # print("check genPart shape")
        # print(genPart.shape)
        genPart = (
            genPart.reset_index("subentry")
            .merge(nJets_acc["nJets_accepted"], on=["entry"], how="left")
            .set_index("subentry", append=True)
        )
        genPart = (
            genPart.reset_index("subentry")
            .merge(nJets_pt["nJets_pt_pass"], on=["entry"], how="left")
            .set_index("subentry", append=True)
        )
        genPart = (
            genPart.reset_index("subentry")
            .merge(nJets_match["nJets_reco"], on=["entry"], how="left")
            .set_index("subentry", append=True)
        )
        genPart = (
            genPart.reset_index("subentry")
            .merge(nJets_ID["nJets_ID"], on=["entry"], how="left")
            .set_index("subentry", append=True)
        )
        genPart = (
            genPart.reset_index("subentry")
            .merge(nJets_btag["nJets_btag"], on=["entry"], how="left")
            .set_index("subentry", append=True)
        )
        genPart.fillna(0, inplace=True)
        genPart = (
            genPart.reset_index("subentry")
            .merge(mm["dimuon_mass"], on=["entry"], how="left")
            .set_index("subentry", append=True)
        )
        genPart.fillna(-999.0, inplace=True)
        genPart = (
            genPart.reset_index("subentry")
            .merge(pt_pass["pt_pass"], on=["entry"], how="left")
            .set_index("subentry", append=True)
        )
        genPart = (
            genPart.reset_index("subentry")
            .merge(acc["accepted"], on=["entry"], how="left")
            .set_index("subentry", append=True)
        )
        genPart = (
            genPart.reset_index("subentry")
            .merge(reco["reco"], on=["entry"], how="left")
            .set_index("subentry", append=True)
        )
        genPart = (
            genPart.reset_index("subentry")
            .merge(ID["ID_pass"], on=["entry"], how="left")
            .set_index("subentry", append=True)
        )
        genPart = (
            genPart.reset_index("subentry")
            .merge(good_pv["gpv"], on=["entry"], how="left")
            .set_index("subentry", append=True)
        )
        genPart.fillna(False, inplace=True)
        genPart = (
            genPart.reset_index("subentry")
            .merge(hlt["hlt"], on=["entry"], how="left")
            .set_index("subentry", append=True)
        )
        genPart = (
            genPart.reset_index("subentry")
            .merge(wgt["wgt_nominal"], on=["entry"], how="left")
            .set_index("subentry", append=True)
        )
        genPart.fillna(0, inplace=True)

        genPart["dataset"] = dataset
        genPart["flavor_reco"] = genPart["flavor_reco"].astype(int)
        genPart["Jet_pt_reco"] = genPart["Jet_pt_reco"].astype(float)
        genPart["Jet_eta_reco"] = genPart["Jet_eta_reco"].astype(float)
        # print(genPart["flavor_reco"])
        if self.apply_to_output is None:
            return genPart
        else:
            self.apply_to_output(genPart)
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
            jet_branches_local += [
                "partonFlavour",
                "hadronFlavour",
                "pt_gen",
                "eta_gen",
                "phi_gen",
            ]
            jets["pt_gen"] = jets.matched_gen.pt
            jets["eta_gen"] = jets.matched_gen.eta
            jets["phi_gen"] = jets.matched_gen.phi
        # if variation == "nominal":
        #    if self.do_jec:
        #        jet_branches += ["pt_jec", "mass_jec"]
        #    if is_mc and self.do_jerunc:
        #        jet_branches += ["pt_orig", "mass_orig"]
        """
        # Find jets that have selected muons within dR<0.4 from them
        #matched_mu_pt = jets.matched_muons.pt_fsr
        #matched_mu_iso = jets.matched_muons.pfRelIso04_all
        #matched_mu_id = jets.matched_muons[self.parameters["muon_id"]]
        #matched_mu_pass = (
        #    (matched_mu_pt > self.parameters["muon_pt_cut"]) &
        #    (matched_mu_iso < self.parameters["muon_iso_cut"]) &
        #    matched_mu_id
        #)
        #clean = ~(ak.to_pandas(matched_mu_pass).astype(float).fillna(0.0)
        #          .groupby(level=[0, 1]).sum().astype(bool))

        # if self.timer:
        #     self.timer.add_checkpoint("Clean jets from matched muons")

        # Select particular JEC variation
        #if '_up' in variation:
        #    unc_name = 'JES_' + variation.replace('_up', '')
        #    if unc_name not in jets.fields:
        #        return
        #    jets = jets[unc_name]['up'][jet_columns]
        #elif '_down' in variation:
        #    unc_name = 'JES_' + variation.replace('_down', '')
        #    if unc_name not in jets.fields:
        #        return
        ##    jets = jets[unc_name]['down'][jet_columns]
        #else:
        """

        # --- conversion from awkward to pandas --- #
        jets = ak.to_pandas(jets[jet_branches_local])

        jets = jets.dropna()
        if jets.index.nlevels == 3:
            # sometimes there are duplicates?
            jets = jets.loc[pd.IndexSlice[:, :, 0], :]
            jets.index = jets.index.droplevel("subsubentry")

        if variation == "nominal":
            # Update pt and mass if JEC was applied
            if self.do_jec:
                jets["pt"] = jets["pt_jec"]
                jets["mass"] = jets["mass_jec"]

            # We use JER corrections only for systematics, so we shouldn't
            # update the kinematics. Use original values,
            # unless JEC were applied.
            if is_mc and self.do_jerunc and not self.do_jec:
                jets["pt"] = jets["pt_orig"]
                jets["mass"] = jets["mass_orig"]

        # ------------------------------------------------------------#
        # Apply jetID and PUID
        # ------------------------------------------------------------#
        # pass_jet_id = jet_id(jets, self.parameters, self.year)
        # pass_jet_puid = jet_puid(jets, self.parameters, self.year)

        # Jet PUID scale factors
        # if is_mc and False:  # disable for now
        #     puid_weight = puid_weights(
        #         self.evaluator, self.year, jets, pt_name,
        #         jet_puid_opt, jet_puid, numevents
        #     )
        #     weights.add_weight('puid_wgt', puid_weight)

        # ------------------------------------------------------------#
        # Select jets
        # ------------------------------------------------------------#
        # jets['clean'] = clean

        # jet_selection = (
        #    pass_jet_id & pass_jet_puid &
        #    (jets.qgl > -2) & jets.clean &
        #    (jets.pt > self.parameters["jet_pt_cut"]) &
        #    (abs(jets.eta) < self.parameters["jet_eta_cut"])
        # )

        # jets = jets[jet_selection]

        # if self.timer:
        #     self.timer.add_checkpoint("Selected jets")

        # ------------------------------------------------------------#
        # Fill jet-related variables
        # ------------------------------------------------------------#

        # njets = jets.reset_index().groupby("entry")["subentry"].nunique()
        # variables["njets"] = njets

        # one_jet = (njets > 0)
        # two_jets = (njets > 1)

        # Sort jets by pT and reset their numbering in an event
        # jets = jets.sort_values(["entry", "pt"], ascending=[True, False])
        jets.index = pd.MultiIndex.from_arrays(
            [jets.index.get_level_values(0), jets.groupby(level=0).cumcount()],
            names=["entry", "subentry"],
        )
        # Select two jets with highest pT

        jets["selection"] = 0
        jets.loc[
            (
                (jets.pt > 30.0)
                & (abs(jets.eta) < 2.4)
                & (jets.btagDeepB > parameters["UL_btag_medium"][self.year])
                & (jets.jetId >= 2)
            ),
            "selection",
        ] = 1
        nBjets = jets.loc[:, "selection"].groupby("entry").sum()
        variables["njets"] = nBjets
        jets = jets.sort_values(["entry", "pt"], ascending=[True, False])
        jet1 = jets.groupby("entry").nth(0)
        jet2 = jets.groupby("entry").nth(1)
        Jets = [jet1, jet2]
        fill_jets(output, variables, Jets, is_mc=is_mc)
        if self.timer:
            self.timer.add_checkpoint("Filled jet variables")
        """
        # ------------------------------------------------------------#
        # Fill soft activity jet variables
        # ------------------------------------------------------------#

        # Effect of changes in jet acceptance should be negligible,
        # no need to calcluate this for each jet pT variation
        #if variation == 'nominal':
        #    fill_softjets(df, output, variables, 2)
        #    fill_softjets(df, output, variables, 5)

            # if self.timer:
            #     self.timer.add_checkpoint("Calculated SA variables")

        # ------------------------------------------------------------#
        # Apply remaining cuts
        # ------------------------------------------------------------#

        # Cut has to be defined here because we will use it in
        # b-tag weights calculation
        #vbf_cut = (
        #    (variables.jj_mass > 400) &
        #    (variables.jj_dEta > 2.5) &
        #    (jet1.pt > 35)
        #)

        # ------------------------------------------------------------#
        # Calculate QGL weights, btag SF and apply btag veto
        # ------------------------------------------------------------#

        #if is_mc and variation == 'nominal':
            # --- QGL weights --- #
        #    isHerwig = ('herwig' in dataset)

        #    qgl_wgts = qgl_weights(
        #        jet1, jet2, isHerwig, output, variables, njets
        #    )
        #    weights.add_weight('qgl_wgt', qgl_wgts, how='all')

            # --- Btag weights --- #
        #    bjet_sel_mask = output.event_selection & two_jets & vbf_cut

        #    btag_wgt, btag_syst = btag_weights(
        #        self, self.btag_lookup, self.btag_systs, jets,
        #        weights, bjet_sel_mask
        #    )
        #    weights.add_weight('btag_wgt', btag_wgt)

            # --- Btag weights variations --- #
        #    for name, bs in btag_syst.items():
        #        weights.add_weight(
        #            f'btag_wgt_{name}', bs, how='only_vars'
        #        )

            # if self.timer:
            #     self.timer.add_checkpoint(
            #         "Applied QGL and B-tag weights"
            #     )

        # Separate from ttH and VH phase space
        #variables['nBtagLoose'] = jets[
        #    (jets.btagDeepB > self.parameters["btag_loose_wp"]) &
        #    (abs(jets.eta) < 2.5)
        #].reset_index().groupby('entry')['subentry'].nunique()

        #variables['nBtagMedium'] = jets[
        #    (jets.btagDeepB > self.parameters["btag_medium_wp"]) &
        #    (abs(jets.eta) < 2.5)
        #].reset_index().groupby('entry')['subentry'].nunique()
        #variables.nBtagLoose = variables.nBtagLoose.fillna(0.0)
        #variables.nBtagMedium = variables.nBtagMedium.fillna(0.0)

        #variables.selection = (
        #    output.event_selection &
        #    (variables.nBtagLoose < 2) &
        #    (variables.nBtagMedium < 1)
        #)

        # ------------------------------------------------------------#
        # Define categories
        # ------------------------------------------------------------#
        #variables['c'] = ''
        #variables.c[
        #    variables.selection & (variables.njets < 2)] = 'ggh_01j'
        #variables.c[
        #    variables.selection &
        #    (variables.njets >= 2) & (~vbf_cut)] = 'ggh_2j'
        #variables.c[
        #    variables.selection &
        #    (variables.njets >= 2) & vbf_cut] = 'vbf'

        # if 'dy' in dataset:
        #     two_jets_matched = np.zeros(numevents, dtype=bool)
        #     matched1 =\
        #         (jet1.matched_genjet.counts > 0)[two_jets[one_jet]]
        #     matched2 = (jet2.matched_genjet.counts > 0)
        #     two_jets_matched[two_jets] = matched1 & matched2
        #     variables.c[
        #         variables.selection &
        #         (variables.njets >= 2) &
        #         vbf_cut & (~two_jets_matched)] = 'vbf_01j'
        #     variables.c[
        #         variables.selection &
        #         (variables.njets >= 2) &
        #         vbf_cut & two_jets_matched] = 'vbf_2j'
        """
        # --------------------------------------------------------------#
        # Fill outputs
        # --------------------------------------------------------------#

        variables.update({"wgt_nominal": weights.get_weight("nominal")})

        # All variables are affected by jet pT because of jet selections:
        # a jet may or may not be selected depending on pT variation.

        for key, val in variables.items():
            output.loc[:, key] = val

        del df
        del muons
        del jets
        del mu1
        del mu2
        return output

    def prepare_lookups(self):
        # Rochester correction
        # rochester_data = txt_converters.convert_rochester_file(
        #    self.parameters["roccor_file"], loaduncs=True
        # )
        # self.roccor_lookup = rochester_lookup.rochester_lookup(rochester_data)
        self.jec_factories, self.jec_factories_data = jec_factories(self.year)
        # Muon scale factors
        self.musf_lookup = musf_lookup(self.parameters)
        # Pile-up reweighting
        self.pu_lookups = pu_lookups(self.parameters)

        # --- Evaluator
        self.extractor = extractor()

        # Z-pT reweigting (disabled)
        zpt_filename = self.parameters["zpt_weights_file"]
        self.extractor.add_weight_sets([f"* * {zpt_filename}"])
        if "2016" in self.year:
            self.zpt_path = "zpt_weights/2016_value"
        else:
            self.zpt_path = "zpt_weights/2017_value"

        # Calibration of event-by-event mass resolution
        for mode in ["Data", "MC"]:
            label = f"res_calib_{mode}_{self.year}"
            path = self.parameters["res_calib_path"]
            file_path = f"{path}/{label}.root"
            self.extractor.add_weight_sets([f"{label} {label} {file_path}"])

        self.extractor.finalize()
        self.evaluator = self.extractor.make_evaluator()

        self.evaluator[self.zpt_path]._axes = self.evaluator[self.zpt_path]._axes[0]
        return

    def postprocess(self, accumulator):
        return accumulator
