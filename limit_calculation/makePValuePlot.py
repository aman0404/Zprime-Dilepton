import ROOT
from ROOT import TPaveLabel, TFile
import sys
sys.path.append('cfgs/')
import os, numpy
from copy import deepcopy
from setTDRStyle import setTDRStyle

def getPValues(fileName):
	
	values = {}
	pValues = []
	masses = []

	file = open(fileName)
	for line in file.readlines():
		mass = str(float(line.split(" ")[0]))
		masses.append(float(mass))
		values[mass]=(float(line.split(" ")[1]))
	masses.sort()	
	for mass in masses:
			pValues.append(values[str(mass)])					
	
	return masses, pValues
	
def getPValuesHybrid(fileName):
	
	values = {}
	pValues = []
	masses = []

	file = open(fileName)
	for line in file.readlines():
		mass = str(float(line.split(" ")[0]))
		masses.append(float(mass))
		if float(line.split(" ")[1]) < 0.5:
			values[mass]=(float(line.split(" ")[1]))
		else:
			values[mass]= 0.5
	masses.sort()	
	for mass in masses:
			pValues.append(values[str(mass)])					
	
	return masses, pValues
			
def countUpcrossings(directory,reference):

	upcrossings = 0
	for fileName in os.listdir(directory):
		m, p = getPValues(directory+"/"+fileName)				
		for index, val in enumerate(p):
			if val < reference and p[index-1] > reference:
				upcrossings += 1 
	return upcrossings


def getMinPValue(fileName):

	minPValue = 0.5
	minPValMass = 0
	m, p = getPValues(fileName)				
	for index, pValue in enumerate(p):
		if pValue < minPValue:
			minPValue = pValue
			minPValMass = m[index]
	
	return minPValue, minPValMass


labels = {"signif": "#Gamma_{Z'}/M_{Z'} = 0.6%","signif006": "#Gamma_{Z'}/M_{Z'} = 0.6%","signif01": "#Gamma_{Z'}/M_{Z'} = 1%","signif03": "#Gamma_{Z'}/M_{Z'} = 3%","signif05": "#Gamma_{Z'}/M_{Z'} = 5%","signif10": "#Gamma_{Z'}/M_{Z'} = 10%"}
lineStyles = {"signif": 1,"signif006": 1,"signif01": 2,"signif03": 3,"signif05": 4,"signif10": 5}
lineColors = {"signif": ROOT.kBlack,"signif006": ROOT.kBlack,"signif01": ROOT.kOrange,"signif03": ROOT.kRed,"signif05": ROOT.kBlue,"signif10": ROOT.kGreen+2}


def main():
	
		import argparse
		parser = argparse.ArgumentParser(usage="makePValuePlot.py [options] -o OUTPUTFILE --card CARD1",description="plots pvalue scans for Z' analysis'",formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	
		parser.add_argument("--card",dest="cards", default=[], action = "append", help='add datacard to list of curves to plot')
		parser.add_argument("--smooth",dest="smooth",action="store_true",default=False, help="Smooth observed values")
		parser.add_argument("-c","--config",dest="config",default='', help="config name")
		parser.add_argument("-t","--tag",dest="tag",default='', help="limit tag")
		parser.add_argument("--ratioLabel",dest="ratioLabel",default='', help="label for ratio")
		args = parser.parse_args()
		
		canv = ROOT.TCanvas("c1","c1",600,450)
		plotPad = ROOT.TPad("plotPad","plotPad",0,0,1,1)
		style = setTDRStyle()
		ROOT.gStyle.SetTitleYOffset(1)
		ROOT.gStyle.SetPadLeftMargin(0.12)
		ROOT.gStyle.SetPadBottomMargin(0.12)
		ROOT.gStyle.SetOptStat(0)
    		ROOT.gStyle.SetTitleXSize(0.055)
    		ROOT.gStyle.SetLabelSize(0.055,"X")
    		ROOT.gStyle.SetLabelSize(0.055,"Y")
   		ROOT.gStyle.SetTitleXOffset(1.05)
    		#ROOT.gStyle.SetLabelYSize(0.04)
    		ROOT.gStyle.SetTitleYSize(0.055)
    		ROOT.gStyle.SetTitleYOffset(1.1)

		plotPad.UseCurrentStyle()
		plotPad.Draw()	
		plotPad.cd()
		plotPad.DrawFrame(200,1e-4,4000,10,";M [GeV]; local p-value")
		plotPad.SetLogy()
	    	#ROOT.gStyle.SetLabelXSize(0.04)
		leg = ROOT.TLegend(0.32, 0.72, 0.9, 0.875,"","brNDC")
		leg.SetFillColor(10)
		leg.SetLineColor(10)
		leg.SetShadowColor(0)
		leg.SetBorderSize(0)		
		leg.SetNColumns(2)		
		leg.SetTextSize(0.06)
		graphs = []
		
		name = "pValues_%s_%s"%(args.config,args.tag)
		fileForHEPData = TFile("plots/"+name+"_forHEPData.root","RECREATE")
		for index, card in enumerate(args.cards):
			if 'width' in card:
				width = "signif"+card.split('width')[-1].split('_')[0]
			else:
				width = 'signif'
		
			masses, pValues = getPValues(card)
			minPVal, minPValMass = getMinPValue(card)
			print card, minPVal, minPValMass 
			graphs.append( ROOT.TGraph(len(masses),numpy.array(masses),numpy.array(pValues)))
			label = card.split("_")[-1].split(".")[0]
			if args.smooth:
				smoother=ROOT.TGraphSmooth("normal")
				graphs[index]=deepcopy(smoother.SmoothSuper(graphs[index],"linear",0,0.005))
				
			graphs[index].SetLineColor(lineColors[width])
			graphs[index].SetLineStyle(lineStyles[width])
			leg.AddEntry(graphs[index],labels[width],"l")			
			graphs[index].Draw("Lsame")	
			graphs[index].SetLineWidth(2)
			graphs[index].SetName("graphPVal%s"%width)
			graphs[index].Write("graphPVal%s"%width)

	

		
		leg.Draw()	
    		leg.SetTextSize(0.045)
		latex = ROOT.TLatex()
		latex.SetTextFont(42)
		latex.SetTextAlign(31)
		latex.SetTextSize(0.03)
		latex.SetNDC(True)
		latexCMS = ROOT.TLatex()
		latexCMS.SetTextFont(62)
		latexCMS.SetTextSize(0.055)
		latexCMS.SetNDC(True)
		latexCMSExtra = ROOT.TLatex()
		latexCMSExtra.SetTextFont(52)
		latexCMSExtra.SetTextSize(0.03)
		latexCMSExtra.SetNDC(True) 

	 	configName = "scanConfiguration_%s"%args.config

        	config =  __import__(configName)
		chan = config.leptons

         	if (chan=="mumu"): 
            		plLumi=TPaveLabel(.65,.885,.9,.99,"140 fb^{-1} (13 TeV, #mu^{+}#mu^{-})","NBNDC")
        	elif (chan=="elel"):
            		plLumi=TPaveLabel(.65,.885,.9,.99,"137 fb^{-1} (13 TeV, ee)","NBNDC")
        	elif (chan=="elmu"):
            		plLumi=TPaveLabel(.27,.885,.9,.99,"137 fb^{-1} (13 TeV, ee) + 140 fb^{-1} (13 TeV, #mu^{+}#mu^{-})","NBNDC")

	    	plLumi.SetTextSize(0.5)
    		plLumi.SetTextFont(42)
    		plLumi.SetFillColor(0)
    		plLumi.SetBorderSize(0)
    		plLumi.Draw()
 

		cmsExtra = "Preliminary"
		latexCMS.DrawLatex(0.14,0.81,"CMS")
		if "Simulation" in cmsExtra:
			yLabelPos = 0.78	
		else:
			yLabelPos = 0.78	
		
		#latexCMSExtra.DrawLatex(0.14,yLabelPos,"%s"%(cmsExtra))			
		
		ZeroSigmaLine = ROOT.TLine(200,0.5,4000,0.5)
		ZeroSigmaLine.SetLineStyle(ROOT.kDashed)
		ZeroSigmaLine.Draw("same")
		
		OneSigmaLine = ROOT.TLine(200,0.317/2,4000,0.317/2)
		OneSigmaLine.SetLineStyle(ROOT.kDashed)
		OneSigmaLine.Draw("same")
		
		TwoSigmaLine = ROOT.TLine(200,0.0455/2,4000,0.0455/2)
		TwoSigmaLine.SetLineStyle(ROOT.kDashed)
		TwoSigmaLine.Draw("same")
		
		ThreeSigmaLine = ROOT.TLine(200,0.0027/2,4000,0.0027/2)
		ThreeSigmaLine.SetLineStyle(ROOT.kDashed)
		ThreeSigmaLine.Draw("same")
		
		FourSigmaLine = ROOT.TLine(200,0.00006/2,4000,0.00006/2)
		FourSigmaLine.SetLineStyle(ROOT.kDashed)
		#~ FourSigmaLine.Draw("same")
		
		FiveSigmaLine = ROOT.TLine(200,3e-07,4000,3e-07)
		FiveSigmaLine.SetLineStyle(ROOT.kDashed)
		#~ FiveSigmaLine.Draw("same")
		
		latex = ROOT.TLatex()
		latex.SetTextFont(42)
		latex.SetTextAlign(31)
		latex.SetTextSize(0.04)
		#~ latex.SetNDC(Tru78		
		latex.DrawLatex(4150, 0.5, "0#sigma")
		latex.DrawLatex(4150, 0.317/2, "1#sigma")
		latex.DrawLatex(4150, 0.0455/2, "2#sigma")
		latex.DrawLatex(4150, 0.0027/2, "3#sigma")
		#~ latex.DrawLatex(4200, 0.00006/2, "4#sigma")
		#~ latex.DrawLatex(4200, 3e-7, "5#sigma")
	
		#~ ROOT.gPad.WaitPrimitive()
		plotPad.SetTicks(1,1)
		plotPad.RedrawAxis()
		if args.smooth:
			name += "_smoothed"
		#name = name+".pdf"
		canv.Print("plots/"+name+".pdf")
		canv.Print("plots/"+name+".root")

		plotPad.RedrawAxis()
		plotPad.SetLogx()
		canv.Print("plots/"+name+"_log.pdf")
		canv.Print("plots/"+name+"_log.root")

   		fileForHEPData.Write()
		fileForHEPData.Close() 


		


main()
