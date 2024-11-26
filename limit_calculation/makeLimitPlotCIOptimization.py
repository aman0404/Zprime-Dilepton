#/usr/bin/env python
import os
import sys
sys.path.append('cfgs/')
from copy import deepcopy
import numpy
import math
import ROOT
from ROOT import TCanvas,TGraphAsymmErrors,TFile,TH1D,TH1F,TGraph,TGraphErrors,gStyle,TLegend,TLine,TGraphSmooth,TPaveText,TGraphAsymmErrors,TPaveLabel,gROOT

ROOT.gROOT.SetBatch(True)

#colors = {"1200":ROOT.kRed+2,"1300":ROOT.kBlue+2,"1400":ROOT.kGreen,"1500":ROOT.kRed,"1600":ROOT.kCyan,"1700":ROOT.kOrange,"1800":ROOT.kBlue,"2100":ROOT.kGreen+2,"2400":ROOT.kOrange+2,"2700":ROOT.kMagenta,"3000":ROOT.kBlack}
colors = {"1000":ROOT.kGreen+3,"2000":ROOT.kRed+2,"2200":ROOT.kBlue+2,"2400":ROOT.kGreen,"2600":ROOT.kRed,"2800":ROOT.kCyan,"1400":ROOT.kOrange,"1800":ROOT.kBlue,"1600":ROOT.kGreen+2,"2400":ROOT.kOrange+2,"2700":ROOT.kMagenta,"3000":ROOT.kBlack}

def getXSecs(name,kFac):
   	smoother=TGraphSmooth("normal")
    	
    	Y={}
    	file=open('tools/xsec_%s.txt'%name,'r')
    	for entries in file:
        	entry=entries.split()
        	X = int(float(entry[0]))
        	Y[X] = float(entry[1])*kFac
	return Y
def getLimitCurve(interference,massCut):

	fileNameExp = "cards/CI_limitCard_Run2CI_Exp_singleBin%sv4_%s.txt"%(massCut,interference) 
    	fileExp=open(fileNameExp,'r')
	limits={}
    	expectedx=[]
    	expectedy=[]
     	for entry in fileExp:
        	massPoint=float(int(entry.split()[0]))
       		limitEntry=float(entry.split()[1])
       		if massPoint not in limits: limits[massPoint]=[]
       		limits[massPoint].append(limitEntry)
	print fileNameExp
    	for massPoint in sorted(limits):
        	limits[massPoint].sort()
        	numLimits=len(limits[massPoint])
        	nrExpts=len(limits[massPoint])
        	medianNr=int(nrExpts*0.5)
 	      	expectedx.append(massPoint)
        	expectedy.append(limits[massPoint][medianNr])
       		expX=numpy.array(expectedx)
    		expY=numpy.array(expectedy)
	print expY
    	GraphExp=TGraph(len(expX),expX,expY)
    	GraphExp.SetLineWidth(3)
    	GraphExp.SetLineStyle(2)
    	GraphExp.SetLineColor(ROOT.kBlue)
	return deepcopy(GraphExp)
def getLimitCurveMultibin(interference,highMass=False):

	xSecs = getXSecs("CI_%s"%interference,1.3)
	fileNameExp = "cards/limitCard_MoriondCI_Exp_massScaleFix2_%s.txt"%(interference) 
	if highMass:
		fileNameExp = "cards/limitCard_MoriondCI_Exp_massScaleFix2_%s.txt"%(interference) 
    	fileExp=open(fileNameExp,'r')
	limits={}
    	expectedx=[]
    	expectedy=[]
     	for entry in fileExp:
        	massPoint=float(int(entry.split()[0]))
       		#limitEntry=float(entry.split()[1])*xSecs[int(float(entry.split()[0]))]
       		limitEntry=float(entry.split()[1])
       		if massPoint not in limits: limits[massPoint]=[]
       		limits[massPoint].append(limitEntry)

    	for massPoint in sorted(limits):
        	limits[massPoint].sort()
        	numLimits=len(limits[massPoint])
        	nrExpts=len(limits[massPoint])
        	medianNr=int(nrExpts*0.5)
 	      	expectedx.append(massPoint)
        	expectedy.append(limits[massPoint][medianNr])
       		expX=numpy.array(expectedx)
    		expY=numpy.array(expectedy)
	print expY
    	GraphExp=TGraph(len(expX),expX,expY)
    	GraphExp.SetLineWidth(3)
    	#GraphExp.SetLineStyle(2)
    	GraphExp.SetLineColor(ROOT.kBlue)
	return deepcopy(GraphExp)



if __name__ == "__main__":
    	import argparse
    	parser = argparse.ArgumentParser(usage="makeLimitPlot.py [options] -o OUTPUTFILE --obs CARD1 --exp CARD2",description="Check if all the ascii files have been produced with the right number of iterations",formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
	massCuts = ['1800','2000','2200','2400','2600','2800',"3000"]
	#massCuts = ['1400','1600','1800','2000','2200','2400','2600','2800']
	#massCuts = ['1200','1300','1400','1500','1600','1700','1800','2100','2400','2700','3000']
	#massCuts = ['1500','1800','2100','2400','2700','3000']
	#massCuts = ['1500','1800','2100','2400']
	
	graphs = {}

	for interference in ['ConLL','ConLR',"ConRL",'ConRR','DesLL',"DesRL",'DesLR','DesRR']:
			cCL=TCanvas("cCL", "cCL",0,0,800,500)
    			gStyle.SetOptStat(0)
	    		plotPad = ROOT.TPad("plotPad","plotPad",0,0,1,1)
    			plotPad.Draw()	
    			plotPad.cd()
			plotPad.SetLogy()
			DummyGraph=TH1F("DummyGraph","",100,10,46)
    			DummyGraph.GetXaxis().SetTitle("#Lambda [TeV]")
        		DummyGraph.GetYaxis().SetTitle("95% CL limit on signal strength mu")
		    	gStyle.SetOptStat(0)
			DummyGraph.GetXaxis().SetRangeUser(10,46)

    			DummyGraph.SetMinimum(0.01)
    			DummyGraph.SetMaximum(20)
    			DummyGraph.GetXaxis().SetLabelSize(0.04)
    			DummyGraph.GetXaxis().SetTitleSize(0.045)
   			DummyGraph.GetXaxis().SetTitleOffset(1.)
    			DummyGraph.GetYaxis().SetLabelSize(0.04)
    			DummyGraph.GetYaxis().SetTitleSize(0.045)
    			DummyGraph.GetYaxis().SetTitleOffset(1.)
    			DummyGraph.Draw()


	
			for massCut in massCuts:
		
				graphs[massCut]=getLimitCurve(interference,massCut)
		    	leg1=TLegend(0.6,0.6,0.9,0.9,"%s"%interference,"brNDC")
			leg1.SetTextSize(0.032)
	

			for index, graph in sorted(graphs.iteritems()):
				graph.Draw("sameL")
				graph.SetLineColor(colors[index])
				leg1.AddEntry(graph,"Mass cut %s GeV"%index,"l")
			#graphMulti = getLimitCurve(interference,massCut)
			#if not "Des" in interference:
			#	graphMulti.Draw("sameL")
#
#				leg1.AddEntry(graphMulti,"multinbin")

			leg1.Draw()
   			cCL.Print("singleBinOptimization_%s.pdf"%interference)
   			cCL.Print("singleBinOptimization_%s.png"%interference)
