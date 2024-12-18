#!/bin/bash

#SBATCH --job-name=SQANTI3
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
module load R/4.3.1 
module load python/3.11.4 
module load miniforge/24.3.0-py3.11
module load perl/5.36.0 
module load star/2.7.9a 
module load kallisto/0.48.0

conda activate SQANTI3.env

chmod +x /project/sheynkman/programs/SQANTI3-5.2/utilities/gtfToGenePred
export PYTHONPATH=$PYTHONPATH:/project/sheynkman/programs/SQANTI3-5.2/cDNA_Cupcake/sequence/
export PYTHONPATH=$PYTHONPATH:/project/sheynkman/programs/SQANTI3-5.2/cDNA_Cupcake/

# mother
python /project/sheynkman/programs/SQANTI3-5.2/sqanti3_qc.py \
01_isoseq/mother/07_rename/Mot.collapsed.gff \
/project/sheynkman/external_data/GENCODE_v46/gencode.v46.basic.annotation.gtf \
/project/sheynkman/external_data/GENCODE_v46/GRCh38.primary_assembly.genome.fa \
--skipORF \
-o Mot \
-d 02_sqanti/mother/ \
--fl_count 01_isoseq/mother/07_rename/Mot.collapsed.abundance.txt

# patient
python /project/sheynkman/programs/SQANTI3-5.2/sqanti3_qc.py \
01_isoseq/patient/06_collapse/Pat.collapsed.gff \
/project/sheynkman/external_data/GENCODE_v46/gencode.v46.basic.annotation.gtf \
/project/sheynkman/external_data/GENCODE_v46/GRCh38.primary_assembly.genome.fa \
--skipORF \
-o Pat \
-d 02_sqanti/patient/ \
--fl_count 01_isoseq/patient/06_collapse/Pat.collapsed.abundance.txt
