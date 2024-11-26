from ROOT import *

import sys
sys.path.append('cfgs/')
import gc 

import glob

for f in glob.glob("userfuncs/*.cxx"):
	gSystem.Load(f)


def getUncert(fileName):
	f = TFile(fileName)
	name = fileName.split("/")[-1].split(".")[0].split("_")[0] + "_" +  fileName.split("/")[-1].split(".")[0].split("_")[1] + "_" +  fileName.split("/")[-1].split(".")[0].split("_")[2]
	w = f.Get(name)
	
	result = w.data("data_%s"%name).numEntries()**0.5/w.data("data_%s"%name).numEntries()
	w = 0
	f.Close()
	gc.collect()
	return result

configName = "scanConfiguration_Run2"

config =  __import__(configName)

i=0
massRange = config.masses[0]
print "from %d to %d in %d GeV steps"%(massRange[1],massRange[2],massRange[0])


colors = [kRed,kGreen,kOrange,kBlack,kBlue,kMagenta,kGreen+3,kOrange+3,kRed+3,kBlue+3,kYellow,kBlue-3]

graphs = []

canv = TCanvas("c1","c1",800,800)
leg = TLegend(0.15,0.4,0.5,0.9,"#Gamma_{Z'} = 0.6%, 4 #sigma window")
for channel in config.channels:
	graphs.append(TGraph())
	mass = massRange[1]
	y =0
	while mass <= massRange[2]:
		fileName = "dataCards_Run2_forStats4/%s_%s.root"%(channel,mass)	

		graphs[i].SetPoint(y,mass,getUncert(fileName))

		gc.collect()
		mass += massRange[0]	
		y += 1		
	graphs[i].SetLineColor(colors[i])
	if i == 0:
		graphs[i].GetYaxis().SetRangeUser(0,0.12)
		graphs[i].GetYaxis().SetTitle('rel. stat. uncert.')
		graphs[i].GetYaxis().SetTitleOffset(1.05)
		graphs[i].GetXaxis().SetTitle('resonance mass [GeV]')

		graphs[i].Draw('AL')
	else:
		graphs[i].Draw('L')
	leg.AddEntry(graphs[i],channel,'l')
	i += 1


leg.Draw()

canv.Print("statsUncert4Sigma.pdf")
