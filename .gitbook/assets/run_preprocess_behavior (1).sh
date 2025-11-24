#!/bin/bash
#SBATCH --job-name=behav_preproc
#SBATCH --output=logs/%x_%A_%a.out   # logs/jobname_jobID_arrayID.out
#SBATCH --time=01:00:00              # adjust as needed
#SBATCH --mem=4G                     # adjust memory as needed
#SBATCH --cpus-per-task=1
#SBATCH --array=0-2   # array over subject list file (3 subjects)
#SBATCH --mail-user=gillian_leblanc@brown.edu
#SBATCH --mail-type=ALL

# ============================
# User configuration
# ============================
BIDS_DIR="/oscar/home/gleblan1/data/Demodat2/xnat-exports/bnc/study-demodat2/bids"        # <--- EDIT THIS PATH
SCRIPT="preprocess_behavior.py"      # Python script path
SUBJ_LIST=$1                         # First argument = text file of subject IDs

# Make sure logs directory exists
mkdir -p logs

# Get subject for this array task
SUBJ=$(sed -n "$((SLURM_ARRAY_TASK_ID+1))p" $SUBJ_LIST)

# Redirect stdout and stderr to log files with subjectID
exec >logs/${SUBJ}_%x_%A_%a.out 2>logs/${SUBJ}_%x_%A_%a.err

echo "SLURM_ARRAY_TASK_ID: $SLURM_ARRAY_TASK_ID"
echo "Processing subject: $SUBJ"

# ----------------------------------------
# Load anaconda module
# ----------------------------------------
module load anaconda

# Optional: activate base or another conda environment if needed
# source activate base
# OR, if you have a custom env:
# conda activate myenv

# Run the Python script
python $SCRIPT --subj $SUBJ --bids_dir $BIDS_DIR
