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

X = np.arange(400, 1950, 50)
Y = np.arange(13, 0.6, -0.40)

def getXSecCurve(chirality,kFac):
    smoother=TGraphSmooth("normal")
    X=[]
    Y=[]
    # X = [6,10,14,18,22,26]
    # Y = [0.03104000 + 0.00384500 + 0.00112200 + 0.00027490, 
    # 0.00827800 + 0.00069630 + 0.00017410 + 0.00003848,
    # 0.00379500 + 0.00025920 + 0.00005577 + 0.00001112,
    # 0.00219300 + 0.00013240 + 0.00002568 + 0.00000467,
    # 0.00144500 + 0.00008064 + 0.00001426 + 0.00000239,
    # 0.00101600 + 0.00005439 + 0.00000909 + 0.00000142]
    if args.BSLL:
      #  X = [1. , 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2. , 2.1, 2.2,
      # 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 3. , 3.1, 3.2, 3.3, 3.4, 3.5,
      # 3.6, 3.7, 3.8, 3.9, 4. , 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8,
      # 4.9, 5. , 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.7, 5.8, 5.9, 6. ]

      #  Y = [2.17139000e-01, 1.48308859e-01, 1.04715953e-01, 7.60263996e-02,
      # 5.65230633e-02, 4.28916543e-02, 3.31327820e-02, 2.59981322e-02,
      # 2.06846327e-02, 1.66618580e-02, 1.35711875e-02, 1.11650495e-02,
      # 9.26930367e-03, 7.75937050e-03, 6.54474706e-03, 5.55875840e-03,
      # 4.75164998e-03, 4.08585337e-03, 3.53269146e-03, 3.07005278e-03,
      # 2.68072840e-03, 2.35120804e-03, 2.07079887e-03, 1.83097356e-03,
      # 1.62488326e-03, 1.44699042e-03, 1.29278954e-03, 1.15859310e-03,
      # 1.04136613e-03, 9.38597526e-04, 8.48199219e-04, 7.68426629e-04,
      # 6.97815596e-04, 6.35132024e-04, 5.79331479e-04, 5.29526597e-04,
      # 4.84960656e-04, 4.44986055e-04, 4.09046691e-04, 3.76663479e-04,
      # 3.47422400e-04, 3.20964595e-04, 2.96978124e-04, 2.75191082e-04,
      # 2.55365836e-04, 2.37294174e-04, 2.20793216e-04, 2.05701951e-04,
      # 1.91878299e-04, 1.79196609e-04, 1.67545525e-04] 
        X = np.arange(400, 1950, 50)
        Y = np.arange(13, 0.6, -0.40)
        #X = [1,2,3,4,5,6]
        # Y = [
        #     0.12610000 + 0.06570000 + 0.02293000 + 0.00251000, # 1
        #     0.00789300 + 0.00408000 + 0.00144200 + 0.00015470, # 2
        #     0.00156600 + 0.00081110 + 0.00028270 + 0.00003061, # 3
        #     0.00009004 + 0.00000957 + 0.00049270 + 0.00025500, # 4
        #     0.00003634 + 0.00000397 + 0.00020190 + 0.00010430, # 5
        #     0.00001769 + 0.00000190 + 0.00009664 + 0.00005067 # 6
        # ]
        
    else: # bbll
        X = [6,10,14,18,22,26]
        if chirality == "posLL":
            Y = [
                0.03104000 + 0.00384500 + 0.00112200 + 0.00027490, 
                0.00827800 + 0.00069630 + 0.00017410 + 0.00003848,
                0.00379500 + 0.00025920 + 0.00005577 + 0.00001112,
                0.00219300 + 0.00013240 + 0.00002568 + 0.00000467,
                0.00144500 + 0.00008064 + 0.00001426 + 0.00000239,
                0.00101600 + 0.00005439 + 0.00000909 + 0.00000142
            ]
        elif chirality == "posLR":
            Y = [
                0.00025760 + 0.00099150 + 0.00790100 + 0.00279500,
                0.00012210 + 0.00003288 + 0.00000000 + 0.00031520,
                0.00002927 + 0.00000835 + 0.00000000 + 0.00006394,
                0.00000949 + 0.00000289 + 0.00000000 + 0.00001461,
                0.00000357 + 0.00000123 + 0.00000000 + 0.00000174,
                0.00000144 + 0.00000059 + 0.00000000 + 0.00000000
            ]
        elif chirality == "posRL":
            Y = [
                0.00103900 + 0.00026760 + 0.01648000 + 0.00318300,
                0.00014050 + 0.00003473 + 0.00303100 + 0.00045890,
                0.00003932 + 0.00000934 + 0.00113900 + 0.00013700,
                0.00001550 + 0.00000356 + 0.00058880 + 0.00005863,
                0.00000755 + 0.00000166 + 0.00036110 + 0.00003090,
                0.00000431 + 0.00000090 + 0.00024380 + 0.00001880
            ]
        elif chirality == "posRR":
            Y = [
                0.00107300 + 0.00027000 + 0.00338300 + 0.02071000,
                0.00015010 + 0.00003593 + 0.00460000 + 0.00052900,
                0.00004434 + 0.00000989 + 0.00191500 + 0.00017280,
                0.00001849 + 0.00000388 + 0.00106000 + 0.00007975,
                0.00000964 + 0.00000188 + 0.00068290 + 0.00004535,
                0.00000576 + 0.00000105 + 0.00047140 + 0.00002902
            ]
        else:
            print("wrong chirality")
            raise ValueError

    aX=numpy.array(X)
    aY=numpy.array(Y)
    #Graph=TGraph(len(X),aX,aY)
    Graph_nonSmooth = TGraph()
    for i in range(0,len(X)):
        Graph_nonSmooth.SetPoint(i,X[i], Y[i])
 
    smooth_exp=TGraphSmooth("normal")
    Graph = smooth_exp.SmoothSuper(Graph_nonSmooth,"linear",0,0.005)

    Graph.SetLineWidth(3)
    Graph.SetLineColor(ROOT.kRed)
    #GraphSmooth=smoother.SmoothSuper(Graph,"linear")
       #GraphSmooth.SetLineWidth(3)
        #GraphSmooth.SetLineColor(lineColors[chirality.split("_")[-1]])
    
    #if SPIN2:
    #		Graph.SetLineColor(colors[chirality])
   #		Graph.SetLineWidth(3)
#		return deepcopy(Graph)
#	else:	
    #return deepcopy(GraphSmooth)
    return deepcopy(Graph)

def getXSecs(kFac):
    """
    not sure what we dowith kFac here
    """

    result = {}
    if args.BSLL:
        result["BSLL"] = {}
        result["BSLL"]["1"] = 0.12610000 + 0.06570000 + 0.02293000 + 0.00251000 # 1
        result["BSLL"]["2"] = 0.00789300 + 0.00408000 + 0.00144200 + 0.00015470 # 2
        result["BSLL"]["3"] = 0.00156600 + 0.00081110 + 0.00028270 + 0.00003061 # 3
        result["BSLL"]["4"] = 0.00009004 + 0.00000957 + 0.00049270 + 0.00025500 # 4
        result["BSLL"]["5"] = 0.00003634 + 0.00000397 + 0.00020190 + 0.00010430 # 5
        result["BSLL"]["6"] = 0.00001769 + 0.00000190 + 0.00009664 + 0.00005067 # 6
    else: # bbll
        result["posLL"] = {}
        result["posLL"]["6"] = 0.03104000 + 0.00384500 + 0.00112200 + 0.00027490
        result["posLL"]["10"] = 0.00827800 + 0.00069630 + 0.00017410 + 0.00003848
        result["posLL"]["14"] = 0.00379500 + 0.00025920 + 0.00005577 + 0.00001112
        result["posLL"]["18"] = 0.00219300 + 0.00013240 + 0.00002568 + 0.00000467
        result["posLL"]["22"] = 0.00144500 + 0.00008064 + 0.00001426 + 0.00000239
        result["posLL"]["26"] = 0.00101600 + 0.00005439 + 0.00000909 + 0.00000142

        result["posLR"] = {}
        result["posLR"]["6"] = 0.00025760 + 0.00099150 + 0.00790100 + 0.00279500
        result["posLR"]["10"] = 0.00012210 + 0.00003288 + 0.00000000 + 0.00031520
        result["posLR"]["14"] = 0.00002927 + 0.00000835 + 0.00000000 + 0.00006394
        result["posLR"]["18"] = 0.00000949 + 0.00000289 + 0.00000000 + 0.00001461
        result["posLR"]["22"] = 0.00000357 + 0.00000123 + 0.00000000 + 0.00000174
        result["posLR"]["26"] = 0.00000144 + 0.00000059 + 0.00000000 + 0.00000000

        result["posRL"] = {}
        result["posRL"]["6"] = 0.00103900 + 0.00026760 + 0.01648000 + 0.00318300
        result["posRL"]["10"] = 0.00014050 + 0.00003473 + 0.00303100 + 0.00045890
        result["posRL"]["14"] = 0.00003932 + 0.00000934 + 0.00113900 + 0.00013700
        result["posRL"]["18"] = 0.00001550 + 0.00000356 + 0.00058880 + 0.00005863
        result["posRL"]["22"] = 0.00000755 + 0.00000166 + 0.00036110 + 0.00003090
        result["posRL"]["26"] = 0.00000431 + 0.00000090 + 0.00024380 + 0.00001880

        result["posRR"] = {}
        result["posRR"]["6"] = 0.00107300 + 0.00027000 + 0.00338300 + 0.02071000
        result["posRR"]["10"] = 0.00015010 + 0.00003593 + 0.00460000 + 0.00052900
        result["posRR"]["14"] = 0.00004434 + 0.00000989 + 0.00191500 + 0.00017280
        result["posRR"]["18"] = 0.00001849 + 0.00000388 + 0.00106000 + 0.00007975
        result["posRR"]["22"] = 0.00000964 + 0.00000188 + 0.00068290 + 0.00004535
        result["posRR"]["26"] = 0.00000576 + 0.00000105 + 0.00047140 + 0.00002902
    # result["bsll"] = {}
    # result["bsll"]["1"] = 0.12610000 + 0.06570000 + 0.02293000 + 0.00251000 # 1
    # result["bsll"]["2"] = 0.00789300 + 0.00408000 + 0.00144200 + 0.00015470 # 2
    # result["bsll"]["3"] = 0.00156600 + 0.00081110 + 0.00028270 + 0.00003061 # 3
    # result["bsll"]["4"] = 0.00009004 + 0.00000957 + 0.00049270 + 0.00025500 # 4
    # result["bsll"]["5"] = 0.00003634 + 0.00000397 + 0.00020190 + 0.00010430 # 5
    # result["bsll"]["6"] = 0.00001769 + 0.00000190 + 0.00009664 + 0.00005067 # 6
    

    return result

lineColors = {"posLL":ROOT.kRed,"posLR":ROOT.kRed,"posRR":ROOT.kRed,"DesLL":ROOT.kBlue,"DesLR":ROOT.kBlue,"DesRR":ROOT.kBlue}
lineStyles = {"posLL":1,"posLR":2,"posRR":4,"DesLL":1,"DesLR":2,"DesRR":4}
# if args.BSLL:
#     labels = {"posLL":"BSLL, constructive left-left","posLR":"CI #rightarrow ll, constructive left-right","posRR":"CI #rightarrow ll, constructive right-right","DesLL":"destructive left-left","DesLR":"destructive left-right","DesRR":"destructive right-right"}
# else:
#     labels = {"posLL":"BBLL, constructive left-left","posLR":"CI #rightarrow ll, constructive left-right","posRR":"CI #rightarrow ll, constructive right-right","DesLL":"destructive left-left","DesLR":"destructive left-right","DesRR":"destructive right-right"}
# labels = {
#     "posLL": {
#         "BBLL" : "BBLL, constructive left-left",
#         "BSLL" : "BSLL, constructive left-left",
#     },
#     "posLR":"CI #rightarrow ll, constructive left-right",
#     "posRR":"CI #rightarrow ll, constructive right-right",
#     "DesLL":"destructive left-left",
#     "DesLR":"destructive left-right",
#     "DesRR":"destructive right-right"
#     }



def printPlots(canvas,name):
        canvas.Print('plots/'+name+".png","png")
        canvas.Print('plots/'+name+".pdf","pdf")
        canvas.SaveSource('plots/'+name+".C","cxx")
        canvas.Print('plots/'+name+".root","root")
        canvas.Print('plots/'+name+".eps","eps")


def results():
    obs = "cards/%s_limitCard_%s_Obs"%(prefix, args.config)
    exp = "cards/%s_limitCard_%s_Exp"%(prefix, args.config)

    observedx=[]
    observedy=[]
    obsLimits={}

    limits={}
    expectedx=[]
    expectedy=[]
    expected1SigLow=[]
    expected1SigHigh=[]
    expected2SigLow=[]
    expected2SigHigh=[]

    if not args.tag == "":
        for mass in range(X):
            mval = str(mass)
            obs += "_m%s_%s_BSLL"%(mval, args.tag)
            exp += "_m%s_%s_BSLL"%(mval, args.tag)

            fileObs=open(obs,'r')
            fileExp=open(exp,'r')

            for entry in fileObs:
                #print("entry: {0}".format(entry))
                print("entry.split()[1]: {0}".format(entry.split()[1]))

                massPoint = mass
                limitEntry=float(entry.split()[1])/137.24
 
                if massPoint not in obsLimits: obsLimits[massPoint]=[]
                    obsLimits[massPoint].append(limitEntry)
                #if printStats: print ("len obsLimits:", len(obsLimits))
                for massPoint in sorted(obsLimits):
                    observedx.append(massPoint)
                    observedy.append(numpy.mean(obsLimits[massPoint]))



            for entry in fileExp:
                massPoint = mThresh
                limitEntry=float(entry.split()[1])/137.24
                #massPoint=float(entry.split()[0])
                #limitEntry=float(entry.split()[1])*xSecs[interference][(str(int(float(entry.split()[0]))))]
                if massPoint not in limits: limits[massPoint]=[]
                    limits[massPoint].append(limitEntry)

                print("limits: {0}".format(limits))
                if printStats: print ("len limits:", len(limits))
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
                    if printStats: print (massPoint,":",limits[massPoint][lower2Sig],limits[massPoint][lower1Sig],limits[massPoint][medianNr],limits[massPoint][upper1Sig],limits[massPoint][upper2Sig])
        #fill lists:
                    expectedx.append(massPoint)
                    print(massPoint, limits[massPoint][medianNr])
                    expectedy.append(limits[massPoint][medianNr])
                    expected1SigLow.append(limits[massPoint][lower1Sig])
                    expected1SigHigh.append(limits[massPoint][upper1Sig])
                    expected2SigLow.append(limits[massPoint][lower2Sig])
                    expected2SigHigh.append(limits[massPoint][upper2Sig])
    
                    expX=numpy.array(expectedx)
                    expY=numpy.array(expectedy)

            
        

def makeLimitPlot(output,obs,exp,chan,interference,printStats=False,obs2="",ratioLabel=""):
    printStats = True
    print("makeLimitPlot")
    fileObs=open(obs,'r')
    fileExp=open(exp,'r')

    observedx=[]
    observedy=[]
    obsLimits={}
    xSecs = getXSecs(1.0)
    print("fileObs:{0}".format(fileObs))
    for entry in fileObs:
        print("entry: {0}".format(entry))
        print("entry.split()[1]: {0}".format(entry.split()[1]))
        print("xSecs[interference]: {0}".format(xSecs[interference]))

        massPoint = mThresh
        limitEntry=float(entry.split()[1])/137.24
        #massPoint=float(entry.split()[0])
        #limitEntry=float(entry.split()[1])*xSecs[interference][(str(int(float(entry.split()[0]))))]
        if massPoint not in obsLimits: obsLimits[massPoint]=[]
        obsLimits[massPoint].append(limitEntry)
        if printStats: print ("len obsLimits:", len(obsLimits))
        for massPoint in sorted(obsLimits):
            observedx.append(massPoint)
            observedy.append(numpy.mean(obsLimits[massPoint]))
            # if (numpy.std(obsLimits[massPoint])/numpy.mean(obsLimits[massPoint])>0.05):
            #         print (massPoint," mean: ",numpy.mean(obsLimits[massPoint])," std dev: ",numpy.std(obsLimits[massPoint])," from: ",obsLimits[massPoint])

    if not obs2 == "":
        fileObs2=open(obs2,'r')

        observedx2=[]
        observedy2=[]
        obsLimits2={}
        for entry in fileObs2:
            massPoint=float(entry.split()[0])
            limitEntry=float(entry.split()[1])*xSecs[interference][(str(int(float(entry.split()[0]))))]
            if massPoint not in obsLimits2: obsLimits2[massPoint]=[]
            obsLimits2[massPoint].append(limitEntry)
        if printStats: print ("len obsLimits:", len(obsLimits2))
        for massPoint in sorted(obsLimits2):
            observedx2.append(massPoint)
            observedy2.append(numpy.mean(obsLimits2[massPoint]))
            # if (numpy.std(obsLimits2[massPoint])/numpy.mean(obsLimits2[massPoint])>0.05):
            #     print (massPoint," mean: ",numpy.mean(obsLimits2[massPoint])," std dev: ",numpy.std(obsLimits2[massPoint])," from: ",obsLimits2[massPoint])





    limits={}
    expectedx=[]
    expectedy=[]
    expected1SigLow=[]
    expected1SigHigh=[]
    expected2SigLow=[]
    expected2SigHigh=[]
    for entry in fileExp:
        massPoint = mThresh
        limitEntry=float(entry.split()[1])/137.24
        #massPoint=float(entry.split()[0])
        #limitEntry=float(entry.split()[1])*xSecs[interference][(str(int(float(entry.split()[0]))))]
        if massPoint not in limits: limits[massPoint]=[]
        limits[massPoint].append(limitEntry)

    print("limits: {0}".format(limits))
    if printStats: print ("len limits:", len(limits))
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
        if printStats: print (massPoint,":",limits[massPoint][lower2Sig],limits[massPoint][lower1Sig],limits[massPoint][medianNr],limits[massPoint][upper1Sig],limits[massPoint][upper2Sig])
        #fill lists:
        expectedx.append(massPoint)
        print (massPoint, limits[massPoint][medianNr])
        expectedy.append(limits[massPoint][medianNr])
        expected1SigLow.append(limits[massPoint][lower1Sig])
        expected1SigHigh.append(limits[massPoint][upper1Sig])
        expected2SigLow.append(limits[massPoint][lower2Sig])
        expected2SigHigh.append(limits[massPoint][upper2Sig])
    
    expX=numpy.array(expectedx)
    expY=numpy.array(expectedy)

    print("aman Xvals here ",expX)
    print("aman Yvals here ",expY)

    values2=[]
    xPointsForValues2=[]
    values=[]
    xPointsForValues=[]
    if printStats: print ("length of expectedx: ", len(expectedx))
    if printStats: print ("length of expected1SigLow: ", len(expected1SigLow))
    if printStats: print ("length of expected1SigHigh: ", len(expected1SigHigh))

    #Here is some Voodoo via Sam:
    for x in range (0,len(expectedx)):
        values2.append(expected2SigLow[x])
        xPointsForValues2.append(expectedx[x])
    for x in range (len(expectedx)-1,0-1,-1):
        values2.append(expected2SigHigh[x])
        xPointsForValues2.append(expectedx[x])
    if printStats: print ("length of values2: ", len(values2))

    for x in range (0,len(expectedx)):
        values.append(expected1SigLow[x])
        xPointsForValues.append(expectedx[x])
    for x in range (len(expectedx)-1,0-1,-1):
        values.append(expected1SigHigh[x])
        xPointsForValues.append(expectedx[x])
    if printStats: print ("length of values: ", len(values))

    exp2Sig=numpy.array(values2)
    xPoints2=numpy.array(xPointsForValues2)
    exp1Sig=numpy.array(values)
    xPoints=numpy.array(xPointsForValues)
    if printStats: print ("xPoints2: ",xPoints2)
    if printStats: print ("exp2Sig: ",exp2Sig)
    if printStats: print ("xPoints: ",xPoints)
    if printStats: print ("exp1Sig: ",exp1Sig)
    GraphErr2Sig=TGraphAsymmErrors(len(xPoints),xPoints2,exp2Sig)
    GraphErr2Sig.SetFillColor(ROOT.kOrange)
    GraphErr1Sig=TGraphAsymmErrors(len(xPoints),xPoints,exp1Sig)
    GraphErr1Sig.SetFillColor(ROOT.kGreen+1)

    cCL=TCanvas("cCL", "cCL",0,0,800,500)
    gStyle.SetOptStat(0)

    if not obs2 == "":
            plotPad = ROOT.TPad("plotPad","plotPad",0,0.3,1,1)
            ratioPad = ROOT.TPad("ratioPad","ratioPad",0,0.,1,0.3)
            plotPad.Draw()	
            ratioPad.Draw()	
            plotPad.cd()
    else:
            plotPad = ROOT.TPad("plotPad","plotPad",0,0,1,1)
            plotPad.Draw()	
            plotPad.cd()


    

    expX=numpy.array(expectedx)
    expY=numpy.array(expectedy)
    print("expX: {0}".format(expX))
    GraphExp=TGraph(len(expX),expX,expY)
    GraphExp.SetLineWidth(3)
    GraphExp.SetLineStyle(2)
    GraphExp.SetLineColor(ROOT.kBlack)

    obsX=numpy.array(observedx)
    obsY=numpy.array(observedy)
    if printStats: print ("obsX: ",obsX)
    if printStats: print ("obsY: ",obsY)

    if SMOOTH:
        smooth_obs=TGraphSmooth("normal")
        GraphObs_nonSmooth=TGraph(len(obsX),obsX,obsY)
        GraphObs=smooth_obs.SmoothSuper(GraphObs_nonSmooth,"linear",0,0.005)
    else:
        GraphObs=TGraph(len(obsX),obsX,obsY)

    GraphObs.SetLineWidth(3)
    if not obs2 == "":
        ratio = []
        ratiox = []
        for index,val in enumerate(observedy):
            mass = observedx[index]
            foundIndex = -1
            for index2, mass2 in enumerate(observedx2):
                if mass == mass2:
                    foundIndex = index2

            if foundIndex > 0:
                ratio.append(observedy2[foundIndex]/val)
                ratiox.append(mass)
        ratioA = numpy.array(ratio)
        ratioX = numpy.array(ratiox)
        obsX2=numpy.array(observedx2)
        obsY2=numpy.array(observedy2)
        ratioGraph = TGraph(len(ratioX),ratioX,ratioA)
        if printStats: print ("obsX2: ",obsX2)
        if printStats: print ("obsY2: ",obsY2)

        if SMOOTH:
            smooth_obs2=TGraphSmooth("normal")
            GraphObs2_nonSmooth=TGraph(len(obsX2),obsX2,obsY2)
            GraphObs2=smooth_obs2.SmoothSuper(GraphObs2_nonSmooth,"linear",0,0.005)
        else:
            GraphObs2=TGraph(len(obsX2),obsX2,obsY2)

        GraphObs2.SetLineWidth(3)

    xSecCurves = []
    xSecCurves.append(getXSecCurve(args.chirality,1)) 

    #Draw the graphs:
    plotPad.SetLogy()
    if args.BSLL:
        lambda_max = 2000
        lambda_min = 400
        yaxis_title_chan = "b #rightarrow sll"
    else: # bbll
        lambda_max = 20
        lambda_min = 6
        yaxis_title_chan = "bb #rightarrow ll"
    DummyGraph=TH1F("DummyGraph","",100,lambda_min,lambda_max)
    DummyGraph.GetXaxis().SetTitle("mass [TeV]")

    #if chan=="mumu":
    #    DummyGraph.GetYaxis().SetTitle("95% CL limit on #sigma({0}) [pb]".format(yaxis_title_chan))
    #elif chan=="elel":
    #    DummyGraph.GetYaxis().SetTitle("95% CL limit on #sigma({0}) [pb]".format(yaxis_title_chan))
    # elif chan=="elmu":
    #     DummyGraph.GetYaxis().SetTitle("95% CL limit on #sigma({0}) [pb]".format(yaxis_title_chan))
    DummyGraph.GetYaxis().SetTitle("#sigma({0})".format(yaxis_title_chan) + " #times #it{#Beta} [pb]")

    gStyle.SetOptStat(0)
    print("args.BSLL: {0}".format(args.BSLL))
    DummyGraph.GetXaxis().SetRangeUser(lambda_min,lambda_max)

    DummyGraph.SetMinimum(5e-5)
    DummyGraph.SetMaximum(10)
    DummyGraph.GetXaxis().SetLabelSize(0.04)
    DummyGraph.GetXaxis().SetTitleSize(0.045)
    DummyGraph.GetXaxis().SetTitleOffset(1.)
    DummyGraph.GetYaxis().SetLabelSize(0.04)
    DummyGraph.GetYaxis().SetTitleSize(0.045)
    DummyGraph.GetYaxis().SetTitleOffset(1.)
    DummyGraph.Draw()
    print("GraphExp.Integral(): {0}".format(GraphExp.Integral()))
    print("GraphExp.GetBinCenter(5): {0}".format(GraphExp.GetXaxis().GetBinCenter(5)))
    print("GraphExp.GetBinCenter(100): {0}".format(GraphExp.GetXaxis().GetBinCenter(100)))
    print("GraphExp.GetNbins(): {0}".format(GraphExp.GetXaxis().GetNbins()))
    # print("GraphExp.GetNbins(): {0}".format(GraphExp.GetBinContent))

    GraphErr2Sig.Draw("F")
    GraphErr1Sig.Draw("F same")
    GraphExp.Draw("lpsame")





#    if (FULL):
#        GraphErr2Sig.Draw("F")
#        GraphErr1Sig.Draw("F")
#        GraphExp.Draw("lpsame")
#    else:
#        if obs2 == "":
#                GraphExp.Draw("lp")
#        if not EXPONLY:
#                GraphObs.Draw("plsame")
#        if not obs2 == "":
#            GraphObs2.SetLineColor(ROOT.kRed)
#            GraphObs2.SetLineStyle(ROOT.kDashed)
#            GraphObs2.Draw("plsame")
    for curve in xSecCurves:
        print ("drawing curve")
        print("curve.Integral(): {0}".format(curve.Integral()))
        print("curve.GetBinCenter(5): {0}".format(curve.GetXaxis().GetBinCenter(5)))
        print("curve.GetBinCenter(100): {0}".format(curve.GetXaxis().GetBinCenter(100)))
        print("curve.GetNbins(): {0}".format(curve.GetXaxis().GetNbins()))
        # print("curve.GetBinContent(100): {0}".format(curve.GetBinContent(100)))
        #curve.Draw("sameC")
        curve.Draw("sameL")


    plCMS=TPaveLabel(.15,.81,.25,.88,"CMS","NBNDC")
    plCMS.SetTextAlign(12)
    plCMS.SetTextFont(62)
    plCMS.SetFillColor(0)
    plCMS.SetFillStyle(0)
    plCMS.SetBorderSize(0)

    plCMS.Draw()

    plPrelim=TPaveLabel(.15,.76,.275,.82,"Preliminary","NBNDC")
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

    labels = {
    # "posLR":"CI #rightarrow ll, constructive left-right",
    # "posRR":"CI #rightarrow ll, constructive right-right",
    "DesLL":"destructive left-left",
    "DesLR":"destructive left-right",
    "DesRR":"destructive right-right"
    }
    # if (chan=="mumu"): 
    #     channel_label = "#mu#mu"
    # elif (chan=="elel"):
    #     channel_label = "ee"
    # elif (chan=="elmu"):
    #     channel_label = "#mu#mu + ee"
    if args.BSLL:
        labels["BSLL"] = "b #rightarrow sll (g=1)"
    else: # bbll
        chirality_map = {
            "posLL" : "LL",
            "posLR" : "LR",
            "posRL" : "RL",
            "posRR" : "RR"
        }
        
        labels[args.chirality] = "bb #rightarrow ll (g=1), constructive {0}".format(chirality_map[args.chirality])


    #leg=TLegend(0.65,0.65,0.87,0.87,"","brNDC")   
    # leg=TLegend(0.440517,0.523051,0.834885,0.878644,"","brNDC")   
#    	leg=TLegend(0.55,0.55,0.87,0.87,"","brNDC")   
    x1 = 0.50
    x2 = x1 + 0.23
    y2 = 0.86
    y1 = 0.60
    leg = TLegend(x1,y1,x2,y2)
    leg.SetFillStyle(0)
    leg.SetBorderSize(0)
    leg.SetTextSize(0.041)
    leg.SetTextFont(42)
    if not obs2 == "":
        if ratioLabel == "":
            ratioLabel = "Variant/Default"
        ratioLabels = ratioLabel.split("/")
        print (ratioLabels)
        leg.AddEntry(GraphObs, "%s Observed 95%% CL limit"%ratioLabels[1],"l")
        leg.AddEntry(GraphObs2,"%s Observed 95%% CL limit"%ratioLabels[0],"l")
        
    else:
        if not EXPONLY:
            leg.AddEntry(GraphObs,"Obs. 95% CL limit","l")
            leg.AddEntry(GraphExp,"Exp. 95% CL limit, median","l")
            if (FULL):
                leg.AddEntry(GraphErr1Sig,"Exp. (68%)","f")
                leg.AddEntry(GraphErr2Sig,"Exp. (95%)","f")
        
        # if args.BSLL:
        #     signal_label = labels[interference]["BSLL"]
        # else: 
        #     signal_label = labels[interference]["BBLL"]
        if (chan=="elmu"):
            leg.SetHeader("95% CL limits (combined)")
        else:
            leg.SetHeader("95% CL limits")
        leg.AddEntry(GraphExp, "Expected",'L')
        # leg.AddEntry(GraphErr1Sig, "#pm 1 std. deviation",'f')
        # leg.AddEntry(GraphErr2Sig, "#pm 2 std. deviation",'f')
        leg.AddEntry(GraphErr1Sig, "Exp. (68%)",'f')
        leg.AddEntry(GraphErr2Sig, "Exp. (95%)",'f')
        leg.AddEntry(xSecCurves[0],labels[interference],"l")
        leg.Draw("hist")

    if "Moriond" in output:
            if (chan=="mumu"): 
                    plLumi=TPaveLabel(.65,.905,.9,.99,"36.3 fb^{-1} (13 TeV, #mu#mu)","NBNDC")
            elif (chan=="elel"):
                    plLumi=TPaveLabel(.65,.905,.9,.99,"35.9 fb^{-1} (13 TeV, ee)","NBNDC")
            elif (chan=="elmu"):
                    plLumi=TPaveLabel(.4,.905,.9,.99,"35.9 fb^{-1} (13 TeV, ee) + 36.3 fb^{-1} (13 TeV, #mu#mu)","NBNDC")

    elif "2017" in output:
            if (chan=="mumu"): 
                plLumi=TPaveLabel(.65,.905,.9,.99,"42.1 fb^{-1} (13 TeV, #mu#mu)","NBNDC")
            elif (chan=="elel"):
                plLumi=TPaveLabel(.65,.905,.9,.99,"41.5 fb^{-1} (13 TeV, ee)","NBNDC")
            elif (chan=="elmu"):            		
                plLumi=TPaveLabel(.4,.905,.9,.99,"41.5 fb^{-1} (13 TeV, ee) + 42.1 fb^{-1} (13 TeV, #mu#mu)","NBNDC")
    else: # 2018, 2017 2016 post and 2016 pre combined
            if (chan=="mumu"): 
                plLumi=TPaveLabel(.65,.905,.9,.99,"138 fb^{-1} (13 TeV, #mu#mu)","NBNDC")
            elif (chan=="elel"):
                plLumi=TPaveLabel(.65,.905,.9,.99,"138 fb^{-1} (13 TeV, ee)","NBNDC")
            elif (chan=="elmu"):
                plLumi=TPaveLabel(.4,.905,.9,.99,"138 fb^{-1} (13 TeV, ee) + 138 fb^{-1} (13 TeV, #mu#mu)","NBNDC")

    plLumi.SetTextSize(0.5)
    plLumi.SetTextFont(42)
    plLumi.SetFillColor(0)
    plLumi.SetBorderSize(0)
    plLumi.Draw()


    plotPad.RedrawAxis()
    plotPad.SetTickx() # set tickes on both sides of the axis
    plotPad.SetTicky() # set tickes on both sides of the axis
    
    if not obs2 == "":

            ratioPad.cd()

            line = ROOT.TLine(200,1,5500,1)
            line.SetLineStyle(ROOT.kDashed)

            ROOT.gStyle.SetTitleSize(0.12, "Y")
            ROOT.gStyle.SetTitleYOffset(0.35) 
            ROOT.gStyle.SetNdivisions(000, "Y")
            ROOT.gStyle.SetNdivisions(408, "Y")
            ratioPad.DrawFrame(200,0.8,5500,1.2, "; ; %s"%ratioLabel)

            line.Draw("same")

            ratioGraph.Draw("sameP")




    
    cCL.Update()
    printPlots(cCL,output)
    

#### ========= MAIN =======================
SMOOTH=False
FULL=True
EXPONLY = False
TWOENERGY=False
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(usage="makeLimitPlot.py [options] -o OUTPUTFILE --obs CARD1 --exp CARD2",description="Check if all the ascii files have been produced with the right number of iterations",formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("--obs",dest="obs", default='', help='Observed datacard')
    parser.add_argument("--obs2",dest="obs2", default='', help='2nd Observed datacard')
    parser.add_argument("--exp",dest="exp", default='', help='Expected datacard')
    parser.add_argument("--stats",dest="stats", action="store_true", default=False, help='Print stats')
    parser.add_argument("--smooth",dest="smooth",action="store_true",default=False, help="Smooth observed values")
    parser.add_argument("--full",dest="full",action="store_true",default=False, help="Draw 2sigma bands")
    parser.add_argument("--expOnly",dest="expOnly",action="store_true",default=False, help="plot only expected")
    parser.add_argument("--BBLL",dest="BBLL",action="store_true",default=False, help="plot BBLL. This option is a bit mute bc this is the default option, but good to have for consistency and readiblility")
    # parser.add_argument("--chir",dest="chirality",default='', help="define chirality if BBLL, ie posLL, posLR, posRL, posRR")
    parser.add_argument("--BSLL",dest="BSLL",action="store_true",default=False, help="plot BSLL")
    parser.add_argument("-c","--config",dest="config",default='', help="config name")
    parser.add_argument("-t","--tag",dest="tag",default='', help="limit tag")
    parser.add_argument("--ratioLabel",dest="ratioLabel",default='', help="label for ratio")
    args = parser.parse_args()
    SMOOTH=args.smooth
    FULL=args.full
    EXPONLY = args.expOnly
    configName = "scanConfiguration_%s"%args.config

    config =  __import__(configName)

    if ("mumu" in config.leptons):  
        print ("Running Limts for dimuon channel")
    elif ("elel" in config.leptons):
        print ("Running Limts for dielectron channel")
    elif ("elmu" in config.leptons):
        print ("Running Limts for Combination of dielectron and dimuon channel")
    else: 
        print ("ERROR, --chan must be mumu, elel or elmu")
        exit

    outputfile = "limitPlotCI_%s"%args.config
    if not args.tag == "":
        outputfile += "_"+args.tag      

    prefix = "BBLL"
    if args.BSLL:
         prefix = "BSLL"    

    obs = "cards/%s_limitCard_%s_Obs"%(prefix, args.config)
    exp = "cards/%s_limitCard_%s_Exp"%(prefix, args.config)
    if not args.tag == "":
        obs += "_" + args.tag
        exp += "_" + args.tag
        print ("Saving histograms in %s" %(outputfile))
        print (" - Obs file: %s" %(obs))
        print (" - Exp file: %s" %(exp))
        if (SMOOTH):
            print ("                  ")
            print ("Smoothing observed lines...")
        print ("\n")


    if args.BSLL:
        interferences = config.interferencesBSLL
    else:    
        interferences = config.interferencesBBLL

    for interference in interferences:
        # obsFile = obs + "_" + interference
        expFile = exp + "_" + interference
        obsFile = expFile
        obsFile += ".txt"
        expFile += ".txt"
        print("obsFile: {0}".format(obsFile))
        print("expFile: {0}".format(expFile))
        print("args.obs: {0}".format(args.obs))
        print("args.exp: {0}".format(args.exp))
        if not args.obs == "":
            obsFile = args.obs
        if not args.exp == "":
            expFile = args.exp

        print("obsFile after: {0}".format(obsFile))
        print("expFile after: {0}".format(expFile))
        print("interference: {0}".format(interference))
        args.chirality = interference
        outName = outputfile+"_"+interference
        makeLimitPlot(outName,obsFile,expFile,config.leptons,interference,args.stats,args.obs2,args.ratioLabel)
        
    
