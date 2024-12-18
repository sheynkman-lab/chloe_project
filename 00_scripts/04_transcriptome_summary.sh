#!/bin/bash

#SBATCH --job-name=transcriptome_summary
#SBATCH --cpus-per-task=10 #number of cores to use
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --time=12:00:00 #amount of time for the whole job
#SBATCH --partition=standard #the queue/partition to run on
#SBATCH --account=sheynkman_lab
#SBATCH --output=%x-%j.log
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=yqy3cu@virginia.edu

# Load necessary modules (if needed)
module purge
module load gcc/11.4.0
module load miniforge/24.3.0-py3.11
module load openmpi/4.1.4
module load python/3.11.4

conda activate transcriptome_sum

# mother
python 00_scripts/04_transcriptome_summary_gene_table_only.py \
--sq_out 03_filter_sqanti/mother/filtered_Mot_classification.tsv \
--ensg_to_gene 01_reference_tables/ensg_gene.tsv \
--enst_to_isoname 01_reference_tables/enst_isoname.tsv \
--odir 04_transcriptome_summary/mother/

# patient
python 00_scripts/04_transcriptome_summary_gene_table_only.py \
--sq_out 03_filter_sqanti/patient/filtered_Pat_classification.tsv \
--ensg_to_gene 01_reference_tables/ensg_gene.tsv \
--enst_to_isoname 01_reference_tables/enst_isoname.tsv \
--odir 04_transcriptome_summary/patient/

conda deactivate