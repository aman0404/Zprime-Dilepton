from ROOT import TCanvas, gStyle, TH1F, gPad



cCL=TCanvas("cCL", "cCL",0,0,600,450)
gStyle.SetOptStat(0)
gStyle.SetPadRightMargin(0.063)
gStyle.SetPadLeftMargin(0.14)
gStyle.SetPadBottomMargin(0.12)


fileExp=open('cards/ZPrime_limitCard_DielectronRun2_Exp_gaus.txt','r')
limits={}
expectedx=[]
expectedy=[]
expected1SigLow=[]
expected1SigHigh=[]
expected2SigLow=[]
expected2SigHigh=[]
masses = []
for entry in fileExp:
	massPoint=float(entry.split()[0])
	limitEntry=float(entry.split()[1])
	if massPoint not in limits: limits[massPoint]=[]
	if massPoint not in masses: masses.append(massPoint)
	limits[massPoint].append(limitEntry)

for mass in masses:
	values = sorted(limits[mass])

	minVal = 0
	maxVal = values[-1]*5

	hist = TH1F('hist%d'%mass,'hist%d'%mass,100,minVal,maxVal)
	for val in values:
		hist.Fill(val)

	hist.GetXaxis().SetTitle('expected limit')

	hist.Draw()

	gPad.SetLogy()
	cCL.Print('expLimits_M%d.pdf'%mass)
	
