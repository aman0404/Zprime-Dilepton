#!/usr/bin/env python

import os
import optparse
#this rather ancient parser is forced upon us by crab (it uses an old version of python)
parser = optparse.OptionParser(description='submits jobs to crab')
parser.add_option('--gridPack')
parser.add_option('--nrJobs',help='nrjobs')
parser.add_option('--nToys',help='number of limits per job')
parser.add_option('--nIter',help='number of iterations in chain')
parser.add_option('--expected',help='calculate expected limits?')
parser.add_option('--inject',help='run with signal injection')
parser.add_option('--mass',help='res mass')
parser.add_option('--outputTag',help='outputTag')
parser.add_option('--crabConfig',help='crab config file to run',default="crab_base.py")
parser.add_option('--config',help='limit config file to run',default="ICHEPDimuon")
options,args = parser.parse_args()

# Sanitize the outputTag to remove leading underscore if not desired
if options.outputTag.startswith('_'):
    options.outputTag = options.outputTag[1:]

print(options.outputTag)

if not options.mass or not options.outputTag or not options.gridPack or not options.nrJobs:
    parser.error("mass, outputTag,config, gridPack, nrJobs are manditory")

outputId = options.outputTag
outputId = outputId+"_"+options.mass
if options.expected==str(1):
	outputFile="expectedLimit_%s_%s_%s.root" % (options.config,options.outputTag,options.mass)
else:	
	outputFile="observedLimit_%s_%s.root" % (options.config,options.outputTag)
#so cmssw var parsing will ignore anything before the first ".py"
#which is why we dont have .py on our script
#and have a dummy arguement which means it'll ignore the 1 passed by crab
#sigh...
print(options.outputTag)

scriptArgs="['dummy=dummy.py','tarFile=%s','outputTag=%s','mass=%s','nIter=%s','nToys=%s','expected=%s','config=%s','inject=%s']" % (options.gridPack,options.outputTag,options.mass,options.nIter,options.nToys,options.expected,options.config,options.inject)
print(scriptArgs)
import datetime
currTime=datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
workingDir="limits_"+outputId+"_"+currTime

with open(options.crabConfig,"r") as configFile:
    configLines = configFile.readlines()
   
tempConfig="crab_base_autoGen.py"

lfnDirBase = '/store/user/amkaur/limits/%s'%options.config

with open(tempConfig,"w") as tempConfigFile:
    for line in configLines:
        line=line.replace("TOSED:SCRIPTARGS",scriptArgs)
        line=line.replace("TOSED:GRIDPACK",options.gridPack)
        line=line.replace("TOSED:OUTPUTFILE",outputFile)
        line=line.replace("TOSED:NRJOBS",options.nrJobs)
        line=line.replace("TOSED:PRIMARYID",options.outputTag)
        line=line.replace("TOSED:SECONDARYID","test")
        line=line.replace("TOSED:REQUESTNAME",workingDir)
        line=line.replace("TOSED:LFNDIRBASE",lfnDirBase)

        tempConfigFile.write(line)




crabSubmitCmd = "crab submit -c "+tempConfig
import os
os.system(crabSubmitCmd)

