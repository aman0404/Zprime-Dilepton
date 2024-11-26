import os
from WMCore.Configuration import Configuration
config = Configuration()

config.section_("General")
config.General.requestName = 'TOSED:REQUESTNAME'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True


config.section_("JobType")
config.JobType.pluginName = 'PrivateMC'
config.JobType.psetName = 'dummyPSet.py'
config.JobType.scriptExe= 'runLimits'
config.JobType.scriptArgs= TOSED:SCRIPTARGS
config.JobType.inputFiles= ['TOSED:GRIDPACK',os.environ['CMSSW_BASE']+'/bin/'+os.environ['SCRAM_ARCH']+'/combine','FrameworkJobReport.xml']
config.JobType.outputFiles= ['TOSED:OUTPUTFILE']
config.JobType.allowUndistributedCMSSW = True
config.JobType.maxMemoryMB = 5000

config.section_("Data")
config.Data.splitting = 'EventBased'
config.Data.unitsPerJob = 1
config.Data.totalUnits = TOSED:NRJOBS
config.Data.outputPrimaryDataset = 'TOSED:PRIMARYID'
config.Data.outputDatasetTag = 'TOSED:SECONDARYID'
config.Data.outLFNDirBase = 'TOSED:LFNDIRBASE'
 
config.section_("Site")
config.Site.storageSite = "T2_US_Purdue"
#config.Site.blacklist = ["T3_US_UCR","T3_MX_Cinvestav","T3_TW_NTU_HEP"]
config.section_("User")
