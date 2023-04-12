class Variable(object):
    def __init__(
        self,
        name_,
        caption_,
        nbins_,
        xmin_,
        xmax_,
        ymin_,
        ymax_,
        binning_=[],
        norm_to_bin_width_=False,
        xminPlot_=None,
        xmaxPlot_=None,
    ):
        self.name = name_
        self.caption = caption_
        self.nbins = nbins_
        self.xmin = xmin_
        self.xmax = xmax_
        self.ymin = ymin_
        self.ymax = ymax_
        if xminPlot_ is not None:
            self.xminPlot = xminPlot_
        else:
            self.xminPlot = xmin_
        if xmaxPlot_ is not None:
            self.xmaxPlot = xmaxPlot_
        else:
            self.xmaxPlot = xmax_
        self.binning = binning_
        self.norm_to_bin_width = norm_to_bin_width_


variables = []

massBinningMuMu = (
    [j for j in range(120, 150, 5)]
    + [j for j in range(150, 200, 10)]
    + [j for j in range(200, 600, 20)]
    + [j for j in range(600, 900, 30)]
    + [j for j in range(900, 1250, 50)]
    + [j for j in range(1250, 1610, 60)]
    + [j for j in range(1610, 1890, 70)]
    + [j for j in range(1890, 3970, 80)]
    + [j for j in range(3970, 6070, 100)]
    + [6070]
)

massBinningEE = (
    [j for j in range(120, 150, 5)]
    + [j for j in range(150, 200, 10)]
    + [j for j in range(200, 600, 20)]
    + [j for j in range(600, 900, 30)]
    + [j for j in range(900, 1250, 50)]
    + [j for j in range(1250, 1610, 60)]
    + [j for j in range(1610, 1890, 70)]
    + [j for j in range(1890, 3970, 80)]
    + [j for j in range(3970, 6070, 100)]
    + [6070]
)

variables.append(
    Variable(
        "dielectron_mass",
        r"$m_{ee}$ [GeV]",
        len(massBinningEE) - 1,
        200,
        1250,
        #4900,
        1e-5,
        1e8,
        binning_=massBinningEE,
        norm_to_bin_width_=True,
    )
)
variables.append(
    Variable(
        "dimuon_mass",
        r"$m_{\mu\mu}$ [GeV]",
        len(massBinningMuMu) - 1,
        200,
        4900,
        1e-5,
        1e8,
        binning_=massBinningMuMu,
        norm_to_bin_width_=True,
    )
)
variables.append(
    Variable(
        "dimuon_mass_resUnc",
        r"$m_{\mu\mu}$ [GeV] (res. unc.)",
        len(massBinningMuMu) - 1,
        200,
        4900,
        1e-5,
        1e8,
        binning_=massBinningMuMu,
        norm_to_bin_width_=True,
    )
)
variables.append(
    Variable(
        "dimuon_mass_scaleUncUp",
        r"$m_{\mu\mu}$ [GeV] (scale unc. up)",
        len(massBinningMuMu) - 1,
        200,
        4900,
        1e-5,
        1e8,
        binning_=massBinningMuMu,
        norm_to_bin_width_=True,
    )
)
variables.append(
    Variable(
        "dimuon_mass_scaleUncDown",
        r"$m_{\mu\mu}$ [GeV] (scale unc. down)",
        len(massBinningMuMu) - 1,
        200,
        4900,
        1e-5,
        1e8,
        binning_=massBinningMuMu,
        norm_to_bin_width_=True,
    )
)
variables.append(
    Variable(
        "dimuon_mass_gen",
        r"generated $m_{\mu\mu}$ [GeV]",
        len(massBinningMuMu) - 1,
        200,
        4900,
        1e-5,
        1e8,
        binning_=massBinningMuMu,
        norm_to_bin_width_=True,
    )
)

variables.append(
    Variable(
        "dielectron_mass_gen",
        r"generated $m_{ee}$ [GeV]",
        len(massBinningEE) - 1,
        200,
        4900,
        1e-5,
        1e8,
        binning_=massBinningEE,
        norm_to_bin_width_=True,
    )
)

variables.append(
    Variable("bmmj1_mass", r"m(\ell\ell b) [GeV]", 200, 0, 4000, 1e-5, 1e8)
)
variables.append(Variable("min_bl_mass", r"min m(l,b) [GeV]", 100, 0, 600, 1e-5, 1e8))
variables.append(
    Variable("min_b1l_mass", r"min m(l,leading b) [GeV]", 100, 0, 600, 1e-5, 1e8)
)
variables.append(
    Variable("min_b2l_mass", r"min m(l,trailing b) [GeV]", 100, 0, 600, 1e-5, 1e8)
)

variables.append(Variable("njets", r"$N_{jet}$", 10, -0.5, 9.5, 0.5, 1e8))
variables.append(Variable("nbjets", r"$N_{b-tagged jet}$", 10, -0.5, 9.5, 0.5, 1e8))
variables.append(
    Variable("met", r"$E_{\mathrm{T}}^{\mathrm{miss}} [GeV]$", 40, 0, 1000, 0.5, 1e8)
)
variables.append(
    Variable("lb_angle", r"$angle_{\ell,b}$", 40, 0, 3.2, 0.01, 1e8)
)


variables.append(
    Variable("bllj1_dR", r"$\Delta R(\ell\ell,b)$", 40, 0, 10, 0.01, 1e8)
)

variables.append(
    #Variable("b1l1_dR", r"$\Delta R(\ell_1,b)$", 200, 0, 1, 0.01, 1e8)
    Variable("b1l1_dR", r"$\Delta R(\ell_1,b)$", 20, 0, 5, 0.01, 1e8)
)

variables.append(
#    Variable("b1l2_dR", r"$\Delta R(\ell_2,b)$", 200, 0, 1, 0.01, 1e8)
    Variable("b1l2_dR", r"$\Delta R(\ell_2,b)$", 20, 0, 5, 0.01, 1e8)
)

variables.append(
    Variable("dielectron_dR", r"$\Delta R(ee)$", 20, 0, 5, 0.01, 1e8)
)

variables.append(
    Variable("dielectron_cos_theta_cs", r"$cos\theta_{\mathrm{CS}}$", 20, -1, 1, 0.5, 1e8)
)
variables.append(
    Variable("bjet1_pt", r"bjet1 p_T [GeV]",100, 0, 500, 1e-5, 1e8)
)
variables.append(
    Variable("bjet2_pt", r"bjet2 p_T [GeV]",100, 0, 500, 1e-5, 1e8)
)
variables.append(
    Variable("mu1_pt", r"\mu_{1} p_T [GeV]",100, 0, 500, 1e-5, 1e8)
)
variables.append(
    Variable("mu2_pt", r"\mu_{2) p_T [GeV]",100, 0, 500, 1e-5, 1e8)
)
variables.append(
    Variable("e1_pt", r"e_{1} p_T [GeV]",100, 0, 500, 1e-5, 1e8)
)
variables.append(
    Variable("e2_pt", r"e_{2) p_T [GeV]",100, 0, 500, 1e-5, 1e8)
)   
variables.append(
    Variable("e1_phi", r"e_{1} {\phi}",16, -4.0, 4.0, 1e-5, 1e8)
)
variables.append(
    Variable("e2_phi", r"e_{2} {\phi}",16, -3.0, 3.0, 1e-5, 1e8)
)
variables.append(
    Variable("e1_eta", r"e_{1} {\eta}",16, -3.0, 3.0, 1e-5, 1e8)
)
variables.append(
    Variable("e2_eta", r"e_{2} {\eta}",16, -3.0, 3.0, 1e-5, 1e8)
)

variables.append(
    Variable("bjet1_eta", r"bjet1 $\eta$",12, -3.0, 3.0, 1e-5, 1e8)
)
variables.append(
    Variable("bjet2_eta", r"bjet2 $\eta$",12, -3.0, 3.0, 1e-5, 1e8)
)


  
variables_lookup = {}
for v in variables:
    variables_lookup[v.name] = v
