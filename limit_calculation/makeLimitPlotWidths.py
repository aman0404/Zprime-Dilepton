#/usr/bin/env python
import os
import sys
import copy
sys.path.append('cfgs/')

import numpy
import math
import ROOT
from ROOT import TCanvas,TGraphAsymmErrors,TFile,TH1D,TH1F,TGraph,TGraphErrors,gStyle,TLegend,TLine,TGraphSmooth,TPaveText,TGraphAsymmErrors,TPaveLabel,gROOT

ROOT.gROOT.SetBatch(True)

def printPlots(canvas,name):
    	canvas.Print('plots/'+name+".png","png")
    	canvas.Print('plots/'+name+".pdf","pdf")
    	canvas.SaveSource('plots/'+name+".C","cxx")
    	canvas.Print('plots/'+name+".root","root")
    	canvas.Print('plots/'+name+".eps","eps")

def createObsGraph(obs):

    	fileObs=open(obs,'r')

    	observedx=[]
    	observedy=[]
    	obsLimits={}
    	for entry in fileObs:
        	massPoint=float(entry.split()[0])
        	limitEntry=float(entry.split()[1])
        	if massPoint not in obsLimits: obsLimits[massPoint]=[]
        	obsLimits[massPoint].append(limitEntry)
    	for massPoint in sorted(obsLimits):
        	observedx.append(massPoint)
        	observedy.append(numpy.mean(obsLimits[massPoint]))
        	if (numpy.std(obsLimits[massPoint])/numpy.mean(obsLimits[massPoint])>0.05):
            		print massPoint," mean: ",numpy.mean(obsLimits[massPoint])," std dev: ",numpy.std(obsLimits[massPoint])," from: ",obsLimits[massPoint]




    	obsX=numpy.array(observedx)
    	obsY=numpy.array(observedy)

    	#if SMOOTH:
       # 	smooth_obs=TGraphSmooth("normal")
       # 	GraphObs_nonSmooth=TGraph(len(obsX),obsX,obsY)
       # 	GraphObs=smooth_obs.SmoothSuper(GraphObs_nonSmooth,"linear",0,0.005)
    #	else:
       	GraphObs=TGraph(len(obsX),obsX,obsY)
    
    	GraphObs.SetLineWidth(3)
	print GraphObs
	return GraphObs

def createExpGraph(exp):

   	fileExp=open(exp,'r')

    	limits={}
    	expectedx=[]
    	expectedy=[]
        for entry in fileExp:
        	massPoint=float(entry.split()[0])
        	limitEntry=float(entry.split()[1])
        	if massPoint not in limits: limits[massPoint]=[]
        	limits[massPoint].append(limitEntry)

    	for massPoint in sorted(limits):
        	limits[massPoint].sort()
        	numLimits=len(limits[massPoint])
        	nrExpts=len(limits[massPoint])
        	medianNr=int(nrExpts*0.5)
        	#get indexes:
    		#fill lists:
        	expectedx.append(massPoint)
        	expectedy.append(limits[massPoint][medianNr])
	print len(expectedx)        
    	expX=numpy.array(expectedx)
    	expY=numpy.array(expectedy)
   	GraphExp=TGraph(len(expX),expX,expY)
    	GraphExp.SetLineWidth(3)
    	GraphExp.SetLineStyle(2)

	return GraphExp

def makeLimitPlot(output,obs,exp,chan,printStats=False):

	fileForHEPData = TFile("plots/"+output+"_forHEPData.root","RECREATE")

	obsLimits = {}
	
	for obsFile in obs:
		if 'width' in obsFile:
			width = obsFile.split('width')[-1].split('_')[0]
		else:
			width = '0.006'
		obsLimits[width] = createObsGraph(obsFile)	

        if  SMOOTH:
		for width,obsGraph in obsLimits.iteritems():
                	smooth_obs=TGraphSmooth("normal")
                	GraphObs_nonSmooth=obsGraph
                	obsLimits[width]=copy.deepcopy(smooth_obs.SmoothSuper(GraphObs_nonSmooth,"linear",0,0.005))
                	obsLimits[width].SetLineWidth(3)


	expLimits = {}
	
	for expFile in exp:
		if 'width' in expFile:
			width = expFile.split('width')[-1].split('_')[0]
		else:
			width = '0.006'	
		expLimits[width] = createExpGraph(expFile)	

    	cCL=TCanvas("cCL", "cCL",0,0,600,450)
    	gStyle.SetOptStat(0)
	gStyle.SetPadRightMargin(0.063)
	gStyle.SetPadLeftMargin(0.14)
	gStyle.SetPadBottomMargin(0.12)
	
    	plotPad = ROOT.TPad("plotPad","plotPad",0,0,1,1)
    	plotPad.Draw()	
    	plotPad.cd()


     	smoother=TGraphSmooth("normal")
    	smoother2=TGraphSmooth("normal")
	   

    
    	zprimeX=[]
    	zprimeY=[]
    	fileZPrime=open('tools/xsec_ssm.txt','r')
    	for entries in fileZPrime:
        	entry=entries.split()
        	zprimeX.append(float(entry[0]))
        	zprimeY.append(float(entry[1])/1928)
    	zpX=numpy.array(zprimeX)
    	zpY=numpy.array(zprimeY)
    	GraphZPrime=TGraph(len(zprimeX),zpX,zpY)
    	GraphZPrimeSmooth=smoother2.SmoothSuper(GraphZPrime,"linear")
    	GraphZPrimeSmooth.SetLineWidth(3)
    	GraphZPrimeSmooth.SetLineColor(ROOT.kGreen+3)
    	GraphZPrimeSmooth.SetLineStyle(2)

    	zprimePsiX=[]
    	zprimePsiY=[]
    	fileZPrimePsi=open('tools/xsec_psi.txt','r')
    	for entries in fileZPrimePsi:
        	entry=entries.split()
        	zprimePsiX.append(float(entry[0]))
        	zprimePsiY.append(float(entry[1])/1928)

   	zpPsiX=numpy.array(zprimePsiX)
	zpPsiY=numpy.array(zprimePsiY)
    	GraphZPrimePsi=TGraph(len(zprimePsiX),zpPsiX,zpPsiY)
    	GraphZPrimePsiSmooth=smoother.SmoothSuper(GraphZPrimePsi,"linear")
   	GraphZPrimePsiSmooth.SetLineWidth(3)
    	GraphZPrimePsiSmooth.SetLineColor(ROOT.kBlue)

#Draw the graphs:
    	plotPad.SetLogy()
    	DummyGraph=TH1F("DummyGraph","",100,200,5500)
    	DummyGraph.GetXaxis().SetTitle("M [GeV]")
	if SPIN2:
        		DummyGraph.GetYaxis().SetTitle("[#sigma#upoint#font[12]{B}] G_{KK} / #sigma#upoint#font[12]{B}] Z")
	else:
        		DummyGraph.GetYaxis().SetTitle("[#sigma#upoint#font[12]{B}] Z' / [#sigma#upoint#font[12]{B}] Z")

#	if SPIN2:
#	    	if chan=="mumu":
#       	 		DummyGraph.GetYaxis().SetTitle("#sigma(pp#rightarrowG_{KK}+X#rightarrow#mu^{+}#mu^{-}+X) / #sigma(pp#rightarrowZ+X#rightarrow#mu^{+}#mu^{-}+X)")
#    		elif chan=="elel":
#        		DummyGraph.GetYaxis().SetTitle("#sigma(pp#rightarrowG_{KK}+X#rightarrowee+X) / #sigma(pp#rightarrowZ+X#rightarrowee+X)")
#    		elif chan=="elmu":
#        		DummyGraph.GetYaxis().SetTitle("#sigma(pp#rightarrowG_{KK}+X#rightarrow#font[12]{ll}+X) / #sigma(pp#rightarrowZ+X#rightarrow#font[12]{ll}+X)")
#	else:
#    		if chan=="mumu":
#        		DummyGraph.GetYaxis().SetTitle("#sigma(pp#rightarrowZ'+X#rightarrow#mu^{+}#mu^{-}+X) / #sigma(pp#rightarrowZ+X#rightarrow#mu^{+}#mu^{-}+X)")
#    		elif chan=="elel":
#        		DummyGraph.GetYaxis().SetTitle("#sigma(pp#rightarrowZ'+X#rightarrowee+X) / #sigma(pp#rightarrowZ+X#rightarrowee+X)")
#    		elif chan=="elmu":
#        		DummyGraph.GetYaxis().SetTitle("#sigma(pp#rightarrowZ'+X#rightarrow#font[12]{ll}+X) / #sigma(pp#rightarrowZ+X#rightarrow#font[12]{ll}+X)")



    	gStyle.SetOptStat(0)
    	DummyGraph.GetXaxis().SetRangeUser(200,5500)

    	DummyGraph.SetMinimum(5e-9)
    	DummyGraph.SetMaximum(1e-3)
    	DummyGraph.GetXaxis().SetLabelSize(0.055)
    	DummyGraph.GetXaxis().SetTitleSize(0.055)
   	DummyGraph.GetXaxis().SetTitleOffset(1.05)
    	DummyGraph.GetYaxis().SetLabelSize(0.055)
    	DummyGraph.GetYaxis().SetTitleSize(0.055)
    	DummyGraph.GetYaxis().SetTitleOffset(1.3)

    	DummyGraph.Draw()
	
    	plCMS=TPaveLabel(.16,.885,.27,.99,"CMS","NBNDC")
#plCMS.SetTextSize(0.8)
    	plCMS.SetTextAlign(12)
    	plCMS.SetTextFont(62)
    	plCMS.SetFillColor(0)
    	plCMS.SetBorderSize(0)
    
    	plCMS.Draw()

    	plPrelim=TPaveLabel(.16,.76,.27,.82,"Preliminary","NBNDC")
    	plPrelim.SetTextSize(0.6)
    	plPrelim.SetTextAlign(12)
    	plPrelim.SetTextFont(52)
    	plPrelim.SetFillColor(0)
    	plPrelim.SetBorderSize(0)
    	#plPrelim.Draw()

    	cCL.SetTickx(1)
    	cCL.SetTicky(1)
    	cCL.RedrawAxis()
    	cCL.Update()
 
    	leg=TLegend(0.420517,0.7,0.85,0.878644,"","brNDC")   
    	legWidth=TLegend(0.625,0.5,0.9,0.7,"width","brNDC")   
#    	leg=TLegend(0.55,0.55,0.87,0.87,"","brNDC")   
    	leg.SetTextSize(0.0425)
    	legWidth.SetTextSize(0.0425)
	colors = {'01':ROOT.kBlue,'03':ROOT.kRed,'05':ROOT.kGreen+3,'10':ROOT.kOrange}
#	for width in sorted(obsLimits):
#		obsGraph = obsLimits[width]
#		if colors.has_key(width):
#			obsGraph.SetLineColor(colors[width])
#		obsGraph.Draw("lsame")
#		if width == '0.006':
#			leg.AddEntry(obsGraph,"Observed 95% CL limit width 0.6%","l")
#		else:	
#			leg.AddEntry(obsGraph,"Observed 95%% CL limit width %d%%"%int(width),"l")
#
#	for width  in sorted(expLimits):
#		expGraph = expLimits[width]
#		if colors.has_key(width):
#			expGraph.SetLineColor(colors[width])
#		expGraph.Draw("lsame")
#		if width == '0.006':
#			leg.AddEntry(expGraph,"Expected 95% CL limit width 0.6%, median","l")
#		else:	
#			leg.AddEntry(expGraph,"Expected 95%% CL limit width %d%%, median"%(int(width)),"l")

	
	for width in sorted(obsLimits):
		obsGraph = obsLimits[width]
		if colors.has_key(width):
			obsGraph.SetLineColor(colors[width])
		obsGraph.Draw("lsame")
		if width == '0.006':
			leg.AddEntry(obsGraph,"Obs. 95% CL limit","l")

	for width  in sorted(expLimits):
		expGraph = expLimits[width]
		if colors.has_key(width):
			expGraph.SetLineColor(colors[width])
		expGraph.Draw("lsame")
		if width == '0.006':
			leg.AddEntry(expGraph,"Exp. 95% CL limit, median","l")
	for width in sorted(obsLimits):
		obsGraph = obsLimits[width]
		if colors.has_key(width):
			obsGraph.SetLineColor(colors[width])
		if width == '0.006':
			legWidth.AddEntry(obsGraph,"0.6%","l")
		else:	
			legWidth.AddEntry(obsGraph,"%d%%"%int(width),"l")


    	if not SPIN2:
        	GraphZPrimeSmooth.Draw("lsame")
        	GraphZPrimePsiSmooth.Draw("lsame")

	leg1=TLegend(0.625,0.35,0.825,0.5,"","brNDC")
	leg1.SetTextSize(0.0375)
	leg1.AddEntry(GraphZPrimeSmooth,"Z'_{SSM} (width 2.97%)","l")	
	leg1.AddEntry(GraphZPrimePsiSmooth,"Z'_{#Psi} (width 0.53%)","l")	
	
    	leg1.SetLineWidth(0)
    	leg1.SetLineStyle(0)
    	leg1.SetLineColor(0)
    	leg1.SetFillStyle(0)
    	leg1.SetBorderSize(0)

	leg1.Draw()

   
    	#plCMS.Draw()
  	plotPad.SetTicks(1,1)
	plotPad.RedrawAxis()	

	

    	leg.SetLineWidth(0)
    	leg.SetLineStyle(0)
    	leg.SetLineColor(0)
    	leg.Draw("hist")
    	legWidth.SetLineWidth(0)
    	legWidth.SetLineStyle(0)
    	legWidth.SetLineColor(0)
    	legWidth.SetFillStyle(0)
	legWidth.SetNColumns(2)
    	legWidth.Draw("hist")


	if "Moriond" in output:
         	if (chan=="mumu"): 
            		plLumi=TPaveLabel(.65,.885,.9,.99,"36.3 fb^{-1} (13 TeV, #mu^{+}#mu^{-})","NBNDC")
        	elif (chan=="elel"):
            		plLumi=TPaveLabel(.65,.885,.9,.99,"35.9 fb^{-1} (13 TeV, ee)","NBNDC")
        	elif (chan=="elmu"):
            		plLumi=TPaveLabel(.27,.885,.9,.99,"35.9 fb^{-1} (13 TeV, ee) + 36.3 fb^{-1} (13 TeV, #mu^{+}#mu^{-})","NBNDC")
	else:
 	      	if (chan=="mumu"): 
            		plLumi=TPaveLabel(.65,.905,.9,.99," 140 fb^{-1} (13 TeV, #mu#mu)","NBNDC")
        	elif (chan=="elel"):
            		plLumi=TPaveLabel(.65,.905,.9,.99,"137 fb^{-1} (13 TeV, ee)","NBNDC")
        	elif (chan=="elmu"):
            		plLumi=TPaveLabel(.4,.905,.9,.99,"137 fb^{-1} (13 TeV, ee) + 140 fb^{-1} (13 TeV, #mu#mu)","NBNDC")


    	plLumi.SetTextSize(0.5)
    	plLumi.SetTextFont(42)
    	plLumi.SetFillColor(0)
    	plLumi.SetBorderSize(0)
    	plLumi.Draw()
    

	plotPad.SetTicks(1,1)
	plotPad.RedrawAxis()

    	cCL.Update()
    	printPlots(cCL,output)
 

	for width in sorted(obsLimits):
		obsGraph = obsLimits[width]
		obsGraph.SetName("graphObs%s"%width)
		obsGraph.Write("graphObs%s"%width)
	for width in sorted(expLimits):
		expGraph = expLimits[width]
		expGraph.SetName("graphExp%s"%width)
		expGraph.Write("graphExp%s"%width)


   	fileForHEPData.Write()
	fileForHEPData.Close() 


    
   

#### ========= MAIN =======================
SMOOTH=False
SPIN2=False
TWOENERGY=False

if __name__ == "__main__":
    	import argparse
    	parser = argparse.ArgumentParser(usage="makeLimitPlot.py [options] -o OUTPUTFILE --obs CARD1 --exp CARD2",description="Check if all the ascii files have been produced with the right number of iterations",formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    	parser.add_argument("--obs",dest="obs", default=[], help='Observed datacards',action='append')
    	parser.add_argument("--exp",dest="exp", default=[], help='Expected datacards',action='append')
    	parser.add_argument("--stats",dest="stats", action="store_true", default=False, help='Print stats')
    	parser.add_argument("--smooth",dest="smooth",action="store_true",default=False, help="Smooth observed values")
    	parser.add_argument("--spin2",dest="spin2",action="store_true",default=False, help="Make Spin2 limits")
    	parser.add_argument("-c","--config",dest="config",default='', help="config name")
    	parser.add_argument("-t","--tag",dest="tag",default='', help="limit tag")
    	parser.add_argument("--ratioLabel",dest="ratioLabel",default='', help="label for ratio")
    	args = parser.parse_args()
    	SMOOTH=args.smooth
    	SPIN2=args.spin2
       
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
	
	outputfile = "limitPlotWidths_%s"%args.config
	if not args.tag == "":
		outputfile += "_"+args.tag        


    	print "Saving histograms in %s" %(outputfile)
    	if (SMOOTH):
        	print "                  "
        	print "Smoothing observed lines..." 
    	print "\n"


	
    	makeLimitPlot(outputfile,args.obs,args.exp,config.leptons,args.stats)
    
