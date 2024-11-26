#/usr/bin/env python
import os
import sys
sys.path.append('cfgs/')
from copy import deepcopy
import numpy
import math
import ROOT
from ROOT import TCanvas,TGraphAsymmErrors,TFile,TH1D,TH1F,TGraph,TGraphErrors,gStyle,TLegend,TLine,TGraphSmooth,TPaveText,TGraphAsymmErrors,TPaveLabel,gROOT, TF1

ROOT.gROOT.SetBatch(True)

def getFittedXSecCurve(name,kFac):

	p0 = 0
	p1 = 0
	if "ConLL" in name:
		p0 = 3.79611
		p1 = 411.605
		#p0 = 7.43293e+06
		#p1 = 13.822
	if "ConLR" in name:
		p0 = 4.99591
		p1 = 331.818
	if "ConRR" in name:
		p0 = 5.99774
		p1 = 656.943
	if "DesLL"in name:
		p0 = -3.81353
		p1 = 345.912
	if "DesLR" in name:
		p0 = -4.09965
		p1 = 324.175
	if "DesRR" in name:
		p0 = -4.76197
		p1 = 705.997
	func = TF1("func","[2]*([0]/x^2+[1]/x^4)",10,40)
	func.SetParameter(0,p0)
	func.SetParameter(1,p1)
	func.SetParameter(2,kFac)
   	func.SetLineWidth(3)
	print func.Eval(28)
    	func.SetLineColor(lineColors[name.split("_")[-1]])
	#GraphSmooth=smoother.SmoothSuper(Graph,"linear")
   	#GraphSmooth.SetLineWidth(3)
    	#GraphSmooth.SetLineColor(lineColors[name.split("_")[-1]])
	
	#if SPIN2:
    #		Graph.SetLineColor(colors[name])
   #		Graph.SetLineWidth(3)
#		return deepcopy(Graph)
#	else:	
	#return deepcopy(GraphSmooth)
	return deepcopy(func)



def getXSecCurve(name,kFac):
   	smoother=TGraphSmooth("normal")
    	X=[]
    	Y=[]
    	file=open('tools/xsec_%s.txt'%name,'r')
    	for entries in file:
        	entry=entries.split()
        	X.append(float(entry[0]))
        	Y.append(float(entry[1])*kFac)
	print Y
   	aX=numpy.array(X)
	aY=numpy.array(Y)
    	Graph=TGraph(len(X),aX,aY)
   	Graph.SetLineWidth(3)
    	Graph.SetLineColor(lineColors[name.split("_")[-1]])
	#GraphSmooth=smoother.SmoothSuper(Graph,"linear")
   	#GraphSmooth.SetLineWidth(3)
    	#GraphSmooth.SetLineColor(lineColors[name.split("_")[-1]])
	
	#if SPIN2:
    #		Graph.SetLineColor(colors[name])
   #		Graph.SetLineWidth(3)
#		return deepcopy(Graph)
#	else:	
	#return deepcopy(GraphSmooth)
	return deepcopy(Graph)
def getXSecs(name,kFac):
   	smoother=TGraphSmooth("normal")
    	
    	Y={}
    	file=open('tools/xsec_%s.txt'%name,'r')
    	for entries in file:
        	entry=entries.split()
        	X = int(float(entry[0]))
        	Y[X] = float(entry[1])*kFac
	return Y


lineColors = {"ConLL":ROOT.kRed,"ConLR":ROOT.kRed,"ConRR":ROOT.kRed,"DesLL":ROOT.kBlue,"DesLR":ROOT.kBlue,"DesRR":ROOT.kBlue}
lineStyles = {"ConLL":1,"ConLR":2,"ConRR":4,"DesLL":1,"DesLR":2,"DesRR":4}
labels = {"ConLL":"constructive left-left","ConLR":"constructive left-right","ConRR":"constructive right-right","DesLL":"destructive left-left","DesLR":"destructive left-right","DesRR":"destructive right-right"}



def printPlots(canvas,name):
    	canvas.Print('plots/'+name+".png","png")
    	canvas.Print('plots/'+name+".pdf","pdf")
    	canvas.SaveSource('plots/'+name+".C","cxx")
    	canvas.Print('plots/'+name+".root","root")
    	canvas.Print('plots/'+name+".eps","eps")



def makeBiasPlot(output,muFile,chan,interference,printStats=False,obs2="",ratioLabel=""):

   	mu=open(muFile,'r')

    	limits={}
    	mux=[]
    	muy=[]
    	mu1SigLow=[]
   	mu1SigHigh=[]
    	mu2SigLow=[]
    	mu2SigHigh=[]
    	for entry in mu:
        	massPoint=float(entry.split()[0])
        	limitEntry=float(entry.split()[1])
        	if massPoint not in limits: limits[massPoint]=[]
        	limits[massPoint].append(limitEntry)

    	if printStats: print "len limits:", len(limits)
    	for massPoint in sorted(limits):
        	limits[massPoint].sort()
        	numLimits=len(limits[massPoint])
        	nrExpts=len(limits[massPoint])
        	medianNr=int(nrExpts*0.5)
        	#get indexes:
        	upper1Sig=int(nrExpts*(1-(1-0.68)*0.5))
        	lower1Sig=int(nrExpts*(1-0.68)*0.5)
        	upper2Sig=int(nrExpts*(1-(1-0.95)*0.5))
        	lower2Sig=int(nrExpts*(1-0.95)*0.5)
        	if printStats: print massPoint,":",limits[massPoint][lower2Sig],limits[massPoint][lower1Sig],limits[massPoint][medianNr],limits[massPoint][upper1Sig],limits[massPoint][upper2Sig]
    		#fill lists:
        	mux.append(massPoint)
		print massPoint, limits[massPoint][medianNr]
        	muy.append(limits[massPoint][medianNr])
        	mu1SigLow.append(limits[massPoint][lower1Sig])
        	mu1SigHigh.append(limits[massPoint][upper1Sig])
        	mu2SigLow.append(limits[massPoint][lower2Sig])
        	mu2SigHigh.append(limits[massPoint][upper2Sig])
        
    	muX=numpy.array(mux)
    	muY=numpy.array(muy)

    	values2=[]
    	xPointsForValues2=[]
    	values=[]
    	xPointsForValues=[]
    	if printStats: print "length of mux: ", len(mux)
    	if printStats: print "length of mu1SigLow: ", len(mu1SigLow)
    	if printStats: print "length of mu1SigHigh: ", len(mu1SigHigh)

	#Here is some Voodoo via Sam:
    	for x in range (0,len(mux)):
        	values2.append(mu2SigLow[x])
        	xPointsForValues2.append(mux[x])
    	for x in range (len(mux)-1,0-1,-1):
        	values2.append(mu2SigHigh[x])
        	xPointsForValues2.append(mux[x])
    	if printStats: print "length of values2: ", len(values2)

    	for x in range (0,len(mux)):
        	values.append(mu1SigLow[x])
        	xPointsForValues.append(mux[x])
    	for x in range (len(mux)-1,0-1,-1):
        	values.append(mu1SigHigh[x])
        	xPointsForValues.append(mux[x])
    	if printStats: print "length of values: ", len(values)

    	mu2Sig=numpy.array(values2)
    	xPoints2=numpy.array(xPointsForValues2)
    	mu1Sig=numpy.array(values)
    	xPoints=numpy.array(xPointsForValues)
    	if printStats: print "xPoints2: ",xPoints2
    	if printStats: print "mu2Sig: ",mu2Sig
    	if printStats: print "xPoints: ",xPoints
    	if printStats: print "mu1Sig: ",mu1Sig
    	GraphErr2Sig=TGraphAsymmErrors(len(xPoints),xPoints2,mu2Sig)
    	GraphErr2Sig.SetFillColor(ROOT.kYellow+1)
    	GraphErr1Sig=TGraphAsymmErrors(len(xPoints),xPoints,mu1Sig)
    	GraphErr1Sig.SetFillColor(ROOT.kGreen)

    	cCL=TCanvas("cCL", "cCL",0,0,800,500)
    	gStyle.SetOptStat(0)

    	plotPad = ROOT.TPad("plotPad","plotPad",0,0,1,1)
    	plotPad.Draw()	
    	plotPad.cd()


    

    	muX=numpy.array(mux)
    	muY=numpy.array(muy)
    	GraphMU=TGraph(len(muX),muX,muY)
    	GraphMU.SetLineWidth(3)
    	GraphMU.SetLineStyle(2)
    	GraphMU.SetLineColor(ROOT.kBlue)

	#Draw the graphs:
	DummyGraph=TH1F("DummyGraph","",100,10,40)
    	DummyGraph.GetXaxis().SetTitle("#Lambda [TeV]")
       	DummyGraph.GetYaxis().SetTitle("#hat{#mu}")
    	gStyle.SetOptStat(0)
	if "Des" in output:
		DummyGraph.GetXaxis().SetRangeUser(10,28)
	else:	
		DummyGraph.GetXaxis().SetRangeUser(10,40)

    	DummyGraph.SetMinimum(-2)
    	DummyGraph.SetMaximum(10)
    	DummyGraph.GetXaxis().SetLabelSize(0.04)
    	DummyGraph.GetXaxis().SetTitleSize(0.045)
   	DummyGraph.GetXaxis().SetTitleOffset(1.)
    	DummyGraph.GetYaxis().SetLabelSize(0.04)
    	DummyGraph.GetYaxis().SetTitleSize(0.045)
    	DummyGraph.GetYaxis().SetTitleOffset(1.)
    	DummyGraph.Draw()
	DummyGraph.SetLineColor(ROOT.kWhite)
    	if (FULL):
        	GraphErr2Sig.Draw("F")
        	GraphErr1Sig.Draw("F")
        	GraphMU.Draw("lpsame")
    	else:
        	GraphMU.Draw("lp")
    	plCMS=TPaveLabel(.12,.81,.22,.88,"CMS","NBNDC")
#plCMS.SetTextSize(0.8)
    	plCMS.SetTextAlign(12)
    	plCMS.SetTextFont(62)
    	plCMS.SetFillColor(0)
    	plCMS.SetFillStyle(0)
    	plCMS.SetBorderSize(0)
    
    	plCMS.Draw()

    	plPrelim=TPaveLabel(.12,.76,.25,.82,"Preliminary","NBNDC")
    	plPrelim.SetTextSize(0.6)
    	plPrelim.SetTextAlign(12)
    	plPrelim.SetTextFont(52)
    	plPrelim.SetFillColor(0)
    	plPrelim.SetFillStyle(0)
    	plPrelim.SetBorderSize(0)
    	plPrelim.Draw()


    	cCL.SetTickx(1)
    	cCL.SetTicky(1)
    	cCL.RedrawAxis()
    	cCL.Update()
    
    	#leg=TLegend(0.65,0.65,0.87,0.87,"","brNDC")   
    	leg=TLegend(0.540517,0.623051,0.834885,0.878644,"","brNDC")   
#    	leg=TLegend(0.55,0.55,0.87,0.87,"","brNDC")   
    	leg.SetTextSize(0.032)
   	leg.AddEntry(GraphMU,"median value","l")
        if (FULL):
   		leg.AddEntry(GraphErr1Sig,"1#sigma quantile","f")
        	leg.AddEntry(GraphErr2Sig,"2#sigma quantile","f")


     	leg.SetLineWidth(0)
    	leg.SetLineStyle(0)
    	leg.SetFillStyle(0)
    	leg.SetLineColor(0)
    	leg.Draw("hist")

 	if "Moriond" in output:
         	if (chan=="mumu"): 
            		plLumi=TPaveLabel(.65,.905,.9,.99,"36.3 fb^{-1} (13 TeV, #mu#mu)","NBNDC")
        	elif (chan=="elel"):
            		plLumi=TPaveLabel(.65,.905,.9,.99,"35.9 fb^{-1} (13 TeV, ee)","NBNDC")
        	elif (chan=="elmu"):
            		plLumi=TPaveLabel(.4,.905,.9,.99,"35.9 fb^{-1} (13 TeV, ee) + 36.3 fb^{-1} (13 TeV, #mu#mu)","NBNDC")
	else:
 	      	if (chan=="mumu"): 
            		plLumi=TPaveLabel(.65,.905,.9,.99,"13.0 fb^{-1} (13 TeV, #mu#mu)","NBNDC")
        	elif (chan=="elel"):
            		plLumi=TPaveLabel(.65,.905,.9,.99,"2.7 fb^{-1} (13 TeV, ee)","NBNDC")
        	elif (chan=="elmu"):
            		plLumi=TPaveLabel(.4,.905,.9,.99,"12.4 fb^{-1} (13 TeV, ee) + 13.0 fb^{-1} (13 TeV, #mu#mu)","NBNDC")

    	plLumi.SetTextSize(0.5)
    	plLumi.SetTextFont(42)
    	plLumi.SetFillColor(0)
    	plLumi.SetBorderSize(0)
    	plLumi.Draw()
	maxX = 40
   	if "Des" in output:
		maxX = 28 
    	line = ROOT.TLine(10,0,maxX,0)
	if "mu1" in output: 
    		line = ROOT.TLine(10,1,maxX,1)
    	line.SetLineStyle(ROOT.kDashed)
   	line.Draw("same")

	plotPad.RedrawAxis()
	



    
    	cCL.Update()
    	printPlots(cCL,output)
    

#### ========= MAIN =======================
SMOOTH=False
FULL=False
EXPONLY = False
TWOENERGY=False
if __name__ == "__main__":
    	import argparse
    	parser = argparse.ArgumentParser(usage="makeLimitPlot.py [options] -o OUTPUTFILE --obs CARD1 --mu CARD2",description="Check if all the ascii files have been produced with the right number of iterations",formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    	parser.add_argument("--mu0",dest="mu0", default='', help='datacard for mu0')
    	parser.add_argument("--obs2",dest="obs2", default='', help='2nd Observed datacard')
    	parser.add_argument("--mu1",dest="mu1", default='', help='datacard for mu2')
    	parser.add_argument("--stats",dest="stats", action="store_true", default=False, help='Print stats')
    	parser.add_argument("--smooth",dest="smooth",action="store_true",default=False, help="Smooth observed values")
    	parser.add_argument("--full",dest="full",action="store_true",default=False, help="Draw 2sigma bands")
    	parser.add_argument("--muOnly",dest="muOnly",action="store_true",default=False, help="plot only mu")
    	parser.add_argument("-c","--config",dest="config",default='', help="config name")
    	parser.add_argument("-t","--tag",dest="tag",default='', help="limit tag")
    	parser.add_argument("--ratioLabel",dest="ratioLabel",default='', help="label for ratio")
    	args = parser.parse_args()
    	SMOOTH=args.smooth
    	FULL=args.full
        EXPONLY = args.muOnly
	configName = "scanConfiguration_%s"%args.config

        config =  __import__(configName)

    	if ("mumu" in config.leptons):  
        	print "Running Limts for dimuon channel"
    	elif ("elel" in config.leptons):
        	print "Running Limts for dielectron channel"
    	elif ("elmu" in config.leptons):
        	print "Running Limts for Combination of dielectron and dimuon channel"
    	else: 
        	print "ERROR, --chan must be mumu, elel or elmu"
        	exit
	
	outputfile = "biasPlotCI_%s"%args.config
	if not args.tag == "":
		outputfile += "_"+args.tag        
	mu0 = "cards/limitCard_%s_Bias_mu0"%args.config 
	mu1 = "cards/limitCard_%s_Bias_mu1"%args.config 
	if not args.tag == "":
		mu0 += "_" + args.tag
		mu1 += "_" + args.tag
    	print "Saving histograms in %s" %(outputfile)
    	print " - Mu0 file: %s" %(mu0)
    	print " - Mu1 file: %s" %(mu1)
    	if (SMOOTH):
        	print "                  "
        	print "Smoothing observed lines..." 
    	print "\n"

	for interference in config.interferences:
		mu0File = mu0 + "_" + interference
		mu1File = mu1 + "_" + interference
		mu0File += ".txt"
		mu1File += ".txt"
		if not args.mu0 == "":
			mu0File = args.mu0
		if not args.mu1 == "":
			mu1File = args.mu1


		outName = outputfile+"_"+interference+"_mu0"
	    	makeBiasPlot(outName,mu0File,config.leptons,interference,args.stats,args.obs2,args.ratioLabel)
		outName = outputfile+"_"+interference+"_mu1"
	    	makeBiasPlot(outName,mu1File,config.leptons,interference,args.stats,args.obs2,args.ratioLabel)
		
    
