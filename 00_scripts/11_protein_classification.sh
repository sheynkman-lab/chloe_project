#!/bin/bash

#SBATCH --job-name=protein_classification
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
python ./00_scripts/11_protein_classification_add_meta.py \
--protein_classification  10_5p_utr/mother/Mot.sqanti_protein_classification_w_5utr_info.tsv \
--best_orf 05_orf_calling/mother/Mot_best_ORF.tsv \
--refined_meta 06_refine_orf_database/mother/Mot_30_orf_refined.tsv \
--ensg_gene 01_reference_tables/ensg_gene.tsv \
--name Mot \
--dest_dir 11_protein_classification/mother/


python ./00_scripts/11_protein_classification.py \
--sqanti_protein 11_protein_classification/mother/Mot.protein_classification_w_meta.tsv \
--name Mot \
--dest_dir 11_protein_classification/mother/

# Patient
python ./00_scripts/11_protein_classification_add_meta.py \
--protein_classification  10_5p_utr/patient/Pat.sqanti_protein_classification_w_5utr_info.tsv \
--best_orf 05_orf_calling/patient/Pat_best_ORF.tsv \
--refined_meta 06_refine_orf_database/patient/Pat_30_orf_refined.tsv \
--ensg_gene ./01_reference_tables/ensg_gene.tsv \
--name Pat \
--dest_dir 11_protein_classification/patient/

python ./00_scripts/11_protein_classification.py \
--sqanti_protein 11_protein_classification/patient/Pat.protein_classification_w_meta.tsv \
--name Pat \
--dest_dir 11_protein_classification/patient/

conda deactivate 
module purge