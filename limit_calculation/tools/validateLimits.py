#!/usr/bin/env python
import math
import os

def getDate(folder):
    subfolders = folder.split("/")
    for i,f in enumerate(subfolders): 
        if ("output" in f):
            break
    date = subfolders[i+1]
    print "Date is %s" %(date)
    return date

def checkObservedLimits(inputfolder):
    ntoys = 6 
    date = getDate(inputfolder)
    warning = []
    error = [] 
    for m in range(400,1000,5):
        filename = inputfolder+"/nchannels_ratio_mcmc_limit_Obs-%s-%s-1.ascii" %(m,date)
        print "Checking for file %s " %(filename)
        if (os.path.isfile(filename)):
            with open(filename) as f:
                if (len(f.readlines()) < ntoys): 
                    warning.append(m)
                    print "[WARNING] Wrong number of toys for %s: only %s instead of %s" %(m,len(f.readlines(),ntoys))
        else: 
            error.append(m)
            print "[ERROR] Missing file for %s " %(m)
                
    for m in range(1000,2000,10):
        filename = inputfolder+"/nchannels_ratio_mcmc_limit_Obs-%s-%s-1.ascii" %(m,date)
        print "Checking for file %s " %(filename)
        if (os.path.isfile(filename)):
            with open(filename) as f:
                if (len(f.readlines()) < ntoys): 
                    warning.append(m)
                    print "[WARNING] Wrong number of toys for %s: only %s instead of %s" %(m,len(f.readlines(),ntoys))
        else: 
            error.append(m)
            print "[ERROR] Missing file for %s " %(m)

    for m in range(2000,3500,20):
        filename = inputfolder+"/nchannels_ratio_mcmc_limit_Obs-%s-%s-1.ascii" %(m,date)
        print "Checking for file %s " %(filename)
        if (os.path.isfile(filename)):
            with open(filename) as f:
                if (len(f.readlines()) < ntoys): 
                    warning.append(m)
                    print "[WARNING] Wrong number of toys for %s: only %s instead of %s" %(m,len(f.readlines(),ntoys))
        else: 
            error.append(m)
            print "[ERROR] Missing file for %s " %(m)

    for m in range(3500,4001,100):
        filename = inputfolder+"/nchannels_ratio_mcmc_limit_Obs-%s-%s-1.ascii" %(m,date)
        print "Checking for file %s " %(filename)        
        if (os.path.isfile(filename)):
            with open(filename) as f:
                if (len(f.readlines()) != ntoys): 
                    warning.append(m)
                    print "[WARNING] Wrong number of toys for %s: only %s instead of %s" %(m,len(f.readlines(),ntoys))
        else: 
            error.append(m)
            print "[ERROR] Missing file for %s " %(m)
            
    print "\n"
    if (len(error)==0):
        print "NO missing files"
    else:
        print "You need to re-run the following mass points, as they are missing: ", error
    if (len(warning)==0): 
        print "All files with the correct number of toys (%s) " %(ntoys)
    else:
        print "You need to re-run (or inspect) the following mass points: ", warning
            
def getFileList(inputfolder,filename):
    files = []

    print inputfolder,filename
    for f in os.listdir(inputfolder):
        if (filename in f) and f.endswith(".ascii"):
            files.append(inputfolder+'/'+f)
    return files

def checkExpectedLimits(inputfolder):
    ntoys = 200
    ntoys_perjob = 20

    warning = []
    error = []
    date = getDate(inputfolder)
    for m in range(400,1000,100):
        filename = "nchannels_ratio_mcmc_limit_Exp-%s-%s" %(m,date)
        files = getFileList(inputfolder,filename)
        ntoys_ran = 0.
        for limitfile in files:
            with open(limitfile) as f:
                ntoys_ran += len(f.readlines()) 
        if (ntoys_ran != ntoys):
            warning.append(m)
            print "[WARNING] Wrong number of toys for %s: only %s instead of %s" %(m,ntoys_ran,ntoys)
        if (len(files)==0): 
            error.append(m)
            print "[ERROR] Missing file for %s " %(m)

    for m in range(1000,4001,250):
        filename = "nchannels_ratio_mcmc_limit_Exp-%s-%s" %(m,date)
        files = getFileList(inputfolder,filename)
        ntoys_ran = 0.
        for limitfile in files:
            with open(limitfile) as f:
                ntoys_ran += len(f.readlines()) 
        if (ntoys_ran != ntoys):
            warning.append(m)
            print "[WARNING] Wrong number of toys for %s: only %s instead of %s" %(m,ntoys_ran,ntoys)
        if (len(files)==0): 
            error.append(m)
            print "[ERROR] Missing file for %s " %(m)

    print "\n"
    if (len(error)==0):
        print "NO missing files"
    else:
        print "You need to re-run the following mass points: ", error
    if (len(warning)==0): 
        print "All files with the correct number of toys (%s) " %(ntoys)
    else:
        print "You need to re-run the following mass points: ", warning

#### ========= MAIN =======================
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(usage="validateLimits.py [options]",description="Check if all the ascii files have been produced with the right number of iterations",formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    parser.add_argument("-i","--ifolder", dest="inputfolder",default="output/", help='Input folder')
    parser.add_argument("--obs",dest="obs", action="store_true", default=False, help='check cards for observed limits')
    parser.add_argument("--exp",dest="exp", action="store_true", default=False, help='check cards for expected limits')
    args = parser.parse_args()
    
    inputfolder = args.inputfolder
    
    if (args.obs) :
        print "Checking Observed limits"
        checkObservedLimits(inputfolder)
    if (args.exp) :
        print "Checkking Expected Limits"
        checkExpectedLimits(inputfolder)

    print "DONE"
