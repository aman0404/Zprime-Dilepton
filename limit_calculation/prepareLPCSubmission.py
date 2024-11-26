def createRunSH(args,config):
	template = '''#!/bin/bash
echo "Starting job on " `date` #Date/time of start of job
echo "Running on: `uname -a`" #Condor job is running on this node
echo "System software: `cat /etc/redhat-release`" #Operating System on that node
source /cvmfs/cms.cern.ch/cmsset_default.sh  ## if a bash script, use .sh instead of .csh
### for case 1. EOS have the following line, otherwise remove this line in case 2.
xrdcp -s root://cmseos.fnal.gov//store/user/%s/CMSSW10213.tgz .
tar -xf CMSSW10213.tgz
rm CMSSW10213.tgz
export SCRAM_ARCH=slc6_amd64_gcc530
cd CMSSW_10_2_13/src/ZPrimeCombine
scramv1 b ProjectRename
eval `scramv1 runtime -sh` # cmsenv is an alias not on the workers
%s -m ${1} -L ${2} -n ${3} # runs the actual calculations
for filename in %s/*.root; do
	fileBase=$(basename $filename)
	%s
done
### remove the output file if you don't want it automatically transferred when the job ends
rm -r dataCards_*
rm -r results_*
cd ${_CONDOR_SCRATCH_DIR}
rm -rf CMSSW_10_2_13
'''
	import subprocess
	from tools import getOutDir
	outDir = getOutDir(args,config)
	
	command = 'python runInterpretation.py -c %s -t %s -r'
	if args.expected:
		command += " -e"
	if args.binned:
		command += " -b"
	if args.signif:
		command += " --signif"
	if args.frequentist:
		command += " --frequentist"
	if args.hybrid:
		command += " --hybrid"
	if args.plc:
		command += " --plc"
	if args.inject:
		command += " -i"
	if args.CI:
		command += " --CI"
	if args.ADD:
		command += " --ADD"
	if args.usePhysicsModel:
		command += " --usePhysicsModel"
	if args.singlebin:
		command += " --singlebin"
	if args.lower:
		command += " --Lower"
	if args.spin2:
		command += " --spin2"
	if args.int:
		command += " --int"

	command = command%(args.config,args.tag.split("_")[-1])
	userName = config.LPCUsername

	subCommand = ["xrdfs", "root://cmseos.fnal.gov", "mkdir", "-p", "%s"%userName, "/store/user/%s/limits/%s"%(userName,outDir)]
	subprocess.call(subCommand)
	print "output director created at /store/user/%s/limits/%s"%(userName,outDir)
	outFile = "higgsCombine%s.%s.mH%d"
	copyCommand = "xrdcp -f %s/${fileBase} root://cmseos.fnal.gov//store/user/%s/limits/%s/${fileBase}"%(outDir,userName,outDir)
	if args.expected:
		copyCommand = "xrdcp -f %s/${fileBase} root://cmseos.fnal.gov//store/user/%s/limits/%s/${fileBase%%.root}_${4}.root"%(outDir,userName,outDir)
	fileName = "runInterpretation.sh"
	if args.expected:
		fileName = "runInterpretationExp.sh"
	text_file = open(fileName, "w")
	text_file.write(template % (userName,command,outDir,copyCommand) )
	text_file.close()


def createJDL(args,config,expMass = -1):

	template='''
universe = vanilla
Executable = %s
Should_Transfer_Files = YES
whenToTransferOutput = ON_EXIT
Transfer_Input_Files = %s
Output = zPrimeCombine_$(Cluster)_$(Process).stdout
Error = zPrimeCombine_$(Cluster)_$(Process).stderr
Log = zPrimeCombine_$(Cluster)_$(Process).log
x509userproxy = $ENV(X509_USER_PROXY)
%s
'''
	queueBlock = ""
	if args.CI or args.ADD:
		if args.expected:
			for L in config.lambdas:
				if L == expMass:
					queueBlock += "Arguments = %d %d %d $(Process)\n"%(args.mass,L,10)
					queueBlock += "Queue %d\n"%(int(config.exptToys/10))		
		else:
			for L in config.lambdas:
				queueBlock += "Arguments = -1 %d %d\n"%(L,config.numToys)
				queueBlock += "Queue 1\n"	

	else:
		if args.expected:
			for massBlock in config.massesExp:
				mass = massBlock[1]
				while mass <= massBlock[2]:
					print mass, expMass
					if mass == expMass:
						queueBlock += "Arguments = %d -1 %d $(Process)\n"%(mass,massBlock[4])
						queueBlock += "Queue %d\n"%massBlock[3]		
					mass += massBlock[0]					
		else:
			for massBlock in config.masses:
				mass = massBlock[1]
				while mass <= massBlock[2]:
					queueBlock += "Arguments = %d -1 %d\n"%(mass,config.numToys)
					queueBlock += "Queue 1\n"	
					mass += massBlock[0]				
	fileName = "runInterpretation.sh"
	if args.expected:
		fileName = "runInterpretationExp.sh"
	text_file = open("condor.jdl", "w")
	text_file.write(template % (fileName,fileName,queueBlock) )
	text_file.close()









