module load anaconda/5.3.1-py37
source activate hmumu
voms-proxy-init --voms cms --valid 72:0:0
source /cvmfs/cms.cern.ch/cmsset_default.sh
source /cvmfs/cms.cern.ch/common/crab-setup.sh
source /cvmfs/sft.cern.ch/lcg/app/releases/ROOT/6.24.00/x86_64-centos7-gcc48-opt/bin/thisroot.sh
export VOMS_PATH=$(echo $(voms-proxy-info | grep path) | sed 's/path.*: //')
export VOMS_USERID=$(echo $(voms-proxy-info | grep path) | sed 's/.*p_u//')
export VOMS_TRG=/home/$USER/x509up_u$VOMS_USERID
cp $VOMS_PATH $VOMS_TRG
echo "Your proxy is copied here: "$VOMS_TRG
export X509_USER_PROXY=$VOMS_TRG
