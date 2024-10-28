#voms-proxy-init --voms cms --valid 192:0:0

source /etc/profile.d/modules.sh
module --force purge 
module load anaconda/2020.11  
conda deactivate                                                                                          

source activate /depot/cms/conda_envs/kaur214/hmumu_root

##not needed
#source activate hmumu
#module use /depot/cms/conda_envs/kaur214/modules/
#module load conda-env/hmumu_root-py3.8.8


##needed
#source /cvmfs/oasis.opensciencegrid.org/osg-software/osg-wn-client/3.6/current/el7-x86_64/setup.sh
source /cvmfs/cms.cern.ch/cmsset_default.sh

voms-proxy-init --voms cms --valid 192:0:0
