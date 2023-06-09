import ROOT

def makeSimpleDatacard():
    '''make a binned datacard to match the 1D ML unfolding.
    This are template datacards no syst.'''
    #inputFile = ROOT.TFile("templates/tmp2016bb_multiBins.root")
    inputFile = ROOT.TFile("templates/tmp2016be_multiBins.root")
    hSR=inputFile.Get("mu_data_obs")
    hCR=inputFile.Get("el_data_obs")
    h_MC_mu = []
    for i in range(11):
        h_MC_mu.append(inputFile.Get("mu_DY_S%d"%i))
    h_MC_el = []
    for i in range(11):
        h_MC_el.append(inputFile.Get("el_DY_S%d"%i))
    h_SR_bkg = inputFile.Get("mu_Other")
    h_CR_bkg = inputFile.Get("el_Other")
    print(hSR.Integral())
    #inputFile.Close()
    print(hSR.Integral())
    #global hGen,hReco,hResp,hBkg
    datacard=open("datacard_templateBased_2016be.txt","w")
    datacard.write("## Automatically generated. Simple C&C datacard model.\n")
    datacard.write("## Original author: Andrea Carlo Marini\n##Adapted for Flavor ratio by Arnab \n")
    datacard.write("* imax\n")
    datacard.write("* jmax\n")
    datacard.write("* kmax\n")
    datacard.write("----------------\n")
    datacard.write("shapes * control templates/tmp2016be_multiBins.root el_$PROCESS\n")
    for i in range(11):
        datacard.write("shapes el_DY_S%d control templates/tmp2016be_multiBins.root $PROCESS $PROCESS$SYSTEMATIC\n" %i)
    datacard.write("shapes el_Other control templates/tmp2016be_multiBins.root $PROCESS $PROCESS$SYSTEMATIC\n")
    datacard.write("shapes * signal templates/tmp2016be_multiBins.root mu_$PROCESS \n")
    for i in range(11):
        datacard.write("shapes mu_DY_S%d signal templates/tmp2016be_multiBins.root $PROCESS $PROCESS$SYSTEMATIC \n" %i)
    datacard.write("shapes mu_Other signal templates/tmp2016be_multiBins.root $PROCESS $PROCESS$SYSTEMATIC \n")
    datacard.write("bin ")
    datacard.write("signal ")
    datacard.write("control ")
    datacard.write("\n")
    datacard.write("observation ")
    datacard.write("%d "%(hSR.Integral()))
    datacard.write("%d "%(hCR.Integral()))
    datacard.write("\n")
    datacard.write("----------------\n")
    datacard.write("bin ")
    for ireco in range(12):
        datacard.write("signal ")
    for ireco in range(12):
        datacard.write("control ")
    datacard.write("\n")
    datacard.write("process ")
    for ireco in range(11):
        datacard.write("mu_DY_S%d "%ireco)
    datacard.write("mu_Other ")
    for ireco in range(11):
        datacard.write("el_DY_S%d "%ireco)
    datacard.write("el_Other ")
    datacard.write("\n")
    datacard.write("process ")
    for ireco in range(11):
        if ireco==0:
            datacard.write("1 ")
        elif ireco==11:
            datacard.write("2 ")
        else:
            datacard.write("%d "%(1-ireco))
    datacard.write("3 ")
    for ireco in range(12):
        datacard.write("%d "%(1+ireco))
    datacard.write("\n")
    datacard.write("rate ")
    for ireco in range(11):
        datacard.write("%.2f "% (h_MC_mu[ireco].Integral()))
    datacard.write("%.2f "%(h_SR_bkg.Integral()))##
    for ireco in range(11):
        datacard.write("%.2f "% (h_MC_el[ireco].Integral()))
    datacard.write("%.2f "%(h_CR_bkg.Integral()))##
    datacard.write("\n")
    datacard.write("----------------\n")


if __name__ == "__main__" :
    makeSimpleDatacard()

