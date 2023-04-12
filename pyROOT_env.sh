source /etc/profile.d/modules.sh
module --force purge 
module load anaconda/2020.11-py38  
conda deactivate                                                                                          

module use /depot/cms/conda_envs/kaur214/modules/
module load conda-env/hmumu_root-py3.8.8

