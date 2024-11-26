import ROOT

rmin = 0 
rmax = 5 
nbins = 500
CL = 0.95
chains = "results_MoriondDimuonCI_chainTest/higgsCombineMoriondDimuonCI.MarkovChainMC.mH1000.root"
#chains = "results_MoriondDimuon_chainTest/higgsCombineMoriondDimuon.MarkovChainMC.mH500.root"

def findSmallestInterval(hist,CL): 

 bins = hist.GetNbinsX()

 best_i = 1
 best_j = 1
 bd = bins+1
 val = 0;

# for i in range(1,bins+1): 
#   integral = hist.GetBinContent(i)
#   for j in range(i+1,bins+2):
#    integral += hist.GetBinContent(j)
#    if integral > CL :
#      val = integral
#      break  
# 
#   if integral > CL and  j-i < bd : 
#     bd = j-i 
#     best_j = j+1 
#     best_i = i
#     val = integral

 integral = 0 
 for i in range(1,bins+1): 
   print integral
   integral += hist.GetBinContent(bins+2-i)
   if integral > CL :
      val = integral
 
      if integral > CL and  i  < bd : 
          bd = i 
          best_i = bins+2-i
          val = integral
      break

 return hist.GetBinLowEdge(best_i), val


fi_MCMC = ROOT.TFile.Open(chains)

# Sum up all of the chains / or could take the average limit
mychain=0
for k in fi_MCMC.Get("toys").GetListOfKeys():
    obj = k.ReadObj
    if mychain ==0: 
        mychain = k.ReadObj().GetAsDataSet()
    else :
        mychain.append(k.ReadObj().GetAsDataSet())

# Easier to fill a histogram why not ?
hist = ROOT.TH1F("h_post",";r;posterior probability",nbins,rmin,rmax)
for i in range(mychain.numEntries()): 
  mychain.get(i)
  hist.Fill(mychain.get(i).getRealValue("Lambda"), mychain.weight())

hist.Scale(1./hist.Integral())
hist.SetLineColor(1)

vl,trueCL = findSmallestInterval(hist,CL)
histCL = hist.Clone()

for b in range(nbins): 
  if histCL.GetBinLowEdge(b+1) > vl: histCL.SetBinContent(b+1,0)
   
c6a = ROOT.TCanvas()

histCL.SetFillColor(ROOT.kAzure-3)
histCL.SetFillStyle(1001)
hist.Draw()
histCL.Draw("histFsame")
hist.Draw("histsame")

ll = ROOT.TLine(vl,0,vl,2*hist.GetBinContent(hist.FindBin(vl))); ll.SetLineColor(2); ll.SetLineWidth(2)

ll.Draw()

print " %g %% (%g %%) interval (target)  = %g < Lambda"%(trueCL,CL,vl)
raw_input()
