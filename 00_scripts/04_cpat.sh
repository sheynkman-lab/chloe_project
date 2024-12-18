#!/bin/bash

#SBATCH --job-name=cpat
#SBATCH --cpus-per-task=10 #number of cores to use
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --time=1:00:00 #amount of time for the whole job
#SBATCH --partition=standard #the queue/partition to run on
#SBATCH --account=sheynkman_lab
#SBATCH --output=%x-%j.log
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=yqy3cu@virginia.edu

# Load necessary modules (if needed)
module purge
module load gcc/11.4.0  
module load openmpi/4.1.4
module load python/3.11.4
module load R/4.3.1
module load miniforge/24.3.0-py3.11


export PATH="$HOME/.local/bin:$PATH"

# mother
cpat \
   -x /project/sheynkman/external_data/CPAT_data/Human_Hexamer.tsv \
   -d /project/sheynkman/external_data/CPAT_data/Human_logitModel.RData \
   -g 03_filter_sqanti/mother/filtered_Mot_corrected.fasta \
   --min-orf=50 \
   --top-orf=50 \
   -o 04_CPAT/mother/Mot \
   2> Mot_cpat.error

# patient
cpat \
   -x /project/sheynkman/external_data/CPAT_data/Human_Hexamer.tsv \
   -d /project/sheynkman/external_data/CPAT_data/Human_logitModel.RData \
   -g 03_filter_sqanti/patient/filtered_Pat_corrected.fasta \
   --min-orf=50 \
   --top-orf=50 \
   -o 04_CPAT/patient/Pat \
   2> Pat_cpat.error