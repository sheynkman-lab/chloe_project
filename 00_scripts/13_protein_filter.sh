#!/bin/bash

#SBATCH --job-name=protein_filter
#SBATCH --cpus-per-task=10 #number of cores to use
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --time=12:00:00 #amount of time for the whole job
#SBATCH --partition=standard #the queue/partition to run on
#SBATCH --account=sheynkman_lab
#SBATCH --output=%x-%j.log
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=yqy3cu@virginia.edu

module load gcc/11.4.0  
module load openmpi/4.1.4
module load python/3.11.4
module load miniforge/24.3.0-py3.11

source $(conda info --base)/etc/profile.d/conda.sh

conda activate protein_class

# Mother
python ./00_scripts/13_protein_filter.py \
--protein_classification 11_protein_classification/mother/Mot.protein_classification.tsv \
--gencode_gtf /project/sheynkman/external_data/GENCODE_v46/gencode.v46.basic.annotation.gtf \
--protein_fasta 12_protein_gene_rename/mother/Mot.protein_refined.fasta \
--sample_cds_gtf 12_protein_gene_rename/mother/Mot_with_cds_refined.gtf \
--min_junctions_after_stop_codon 2 \
--name 13_protein_filter/mother/Mot

# Patient
python ./00_scripts/13_protein_filter.py \
--protein_classification 11_protein_classification/patient/Pat.protein_classification.tsv \
--gencode_gtf /project/sheynkman/external_data/GENCODE_v46/gencode.v46.basic.annotation.gtf \
--protein_fasta 12_protein_gene_rename/patient/Pat.protein_refined.fasta \
--sample_cds_gtf 12_protein_gene_rename/patient/Pat_with_cds_refined.gtf \
--min_junctions_after_stop_codon 2 \
--name 13_protein_filter/patient/Pat

conda deactivate
module purge