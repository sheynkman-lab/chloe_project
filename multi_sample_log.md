# Chloe Project
This project is comparing protein isoforms identified by long-read proteogenomics between a patient and mother.  <br />

## Make directory structure and prepare the data 
The data were delivered by PacBio in a way that the mother and patient data are separated. The PB accession numbers are not compatible, so I will reassign them later in the pipeline. <br />
```
cd /project/sheynkman/users/emily/chloe_project

mkdir 00_scripts/
mkdir 01_mandalorion/
mkdir 01_isoquant/
mkdir 01_reference_tables/
mkdir 02_sqanti/
mkdir 02_make_gencode_database/
mkdir 03_filter_sqanti/
mkdir 04_CPAT/
mkdir 04_transcriptome_summary/
mkdir 05_orf_calling/
mkdir 06_refine_orf_database/
mkdir 07_make_cds_gtf/
mkdir 08_rename_cds_to_exon/
mkdir 09_sqanti_protein/
mkdir 10_5p_utr/
mkdir 11_protein_classification/
mkdir 12_protein_gene_rename/
mkdir 13_protein_filter/
mkdir 14_protein_hybrid_database/
mkdir 17_track_visualization/
mkdir 18_SUPPA/
mkdir 19_LRP_summary/

mkdir 01_mandalorion/mother/
mkdir 01_isoquant/mother/
mkdir 02_sqanti/mother/
mkdir 03_filter_sqanti/mother/
mkdir 04_CPAT/mother/
mkdir 04_transcriptome_summary/mother/
mkdir 05_orf_calling/mother/
mkdir 06_refine_orf_database/mother/
mkdir 07_make_cds_gtf/mother/
mkdir 08_rename_cds_to_exon/mother/
mkdir 09_sqanti_protein/mother/
mkdir 10_5p_utr/mother/
mkdir 11_protein_classification/mother/
mkdir 12_protein_gene_rename/mother/
mkdir 13_protein_filter/mother/
mkdir 14_protein_hybrid_database/mother/
mkdir 17_track_visualization/mother/

mkdir 01_mandalorion/patient/
mkdir 01_isoquant/patient/
mkdir 02_sqanti/patient/
mkdir 03_filter_sqanti/patient/
mkdir 04_CPAT/patient/
mkdir 04_transcriptome_summary/patient/
mkdir 05_orf_calling/patient/
mkdir 06_refine_orf_database/patient/
mkdir 07_make_cds_gtf/patient/
mkdir 08_rename_cds_to_exon/patient/
mkdir 09_sqanti_protein/patient/
mkdir 10_5p_utr/patient/
mkdir 11_protein_classification/patient/
mkdir 12_protein_gene_rename/patient/
mkdir 13_protein_filter/patient/
mkdir 14_protein_hybrid_database/patient/
mkdir 17_track_visualization/patient/
```

## Step 01 - Iso-Sew & Transcript Harmonization
Run isoseq and harmonize the PB Accessions between mother and patient data. <br />
```
sbatch 00_scripts/01_isoseq.sh
#sbatch 00_scripts/01.7_rename_transcripts.sh
```

## Step 02 - SQANTI3
```
sbatch 00_scripts/02_sqanti.sh
```

## Step 03 - Filter SQANTI3
```
sbatch 00_scripts/03_filter_sqanti.sh
```

## Step 04 - CPAT
```
sbatch 00_scripts/04_cpat.sh
```

## Step 04 - Transcriptome Summary
```
sbatch 00_scripts/04_transcriptome_summary.sh
```

## Step 05 - ORF Calling
```
sbatch 00_scripts/05_orf_calling.sh
```

## Step 06 - Refine ORF Database
```
sbatch 00_scripts/06_refine_orf_database.sh
```

## Step 07 - Make CDS GTF
```
sbatch 00_scripts/07_make_cds_gtf.sh

python 00_scripts/harmonize_PB.py
```

## Step 08 - Rename CDS to Exon
```
sbatch 00_scripts/08_rename_cds_to_exon.sh
```

## Step 09 - SQANTI Protein
```
sbatch 00_scripts/09_sqanti_protein.sh
```

## Step 10 - 5' UTR
```
sbatch 00_scripts/10_5p_utr.sh
```

## Step 11 - Protein Classification
```
sbatch 00_scripts/11_protein_classification.sh
```

## Step 12 - Protein Gene Rename
```
sbatch 00_scripts/12_protein_gene_rename.sh
```

## Step 13 - Protein Filter
```
sbatch 00_scripts/13_protein_filter.sh
```

## Step 14 - Protein Hybrid Database
```
sbatch 00_scripts/14_protein_hybrid_database.sh
```
Skip intermediate steps because no MS data is available. <br />

## 17 - Track visualization
This step is more run by run customizable, so I'll do it manually
```
module purge
module load gcc/11.4.0  
module load openmpi/4.1.4
module load python/3.11.4
module load miniforge/24.3.0-py3.11

conda activate visualization

# Mother - RGB code (219,076,119)
# Refined Transcripts
gtfToGenePred 07_make_cds_gtf/mother/Mot_cds.gtf 17_track_visualization/mother/Mot_refined_cds.genePred
genePredToBed 17_track_visualization/mother/Mot_refined_cds.genePred 17_track_visualization/mother/Mot_refined_cds.bed12

python ./00_scripts/17_add_rgb_to_bed.py \
--input_bed 17_track_visualization/mother/Mot_refined_cds.bed12 \
--output_dir 17_track_visualization/mother \
--rgb 219,076,119

# Filtered Proteins
gtfToGenePred 13_protein_filter/mother/Mot_with_cds_filtered.gtf 17_track_visualization/mother/Mot_filtered_proteins.genePred
genePredToBed 17_track_visualization/mother/Mot_filtered_proteins.genePred 17_track_visualization/mother/Mot_filtered_proteins.bed12

python ./00_scripts/17_add_rgb_to_bed.py \
--input_bed 17_track_visualization/mother/Mot_filtered_proteins.bed12 \
--output_dir 17_track_visualization/mother \
--rgb 219,076,119

# Patient - RGB code (016,085,154)
# Refined Transcripts
gtfToGenePred 07_make_cds_gtf/patient/Pat_cds_updated.gtf 17_track_visualization/patient/Pat_refined_cds.genePred
genePredToBed 17_track_visualization/patient/Pat_refined_cds.genePred 17_track_visualization/patient/Pat_refined_cds.bed12

python ./00_scripts/17_add_rgb_to_bed.py \
--input_bed 17_track_visualization/patient/Pat_refined_cds.bed12 \
--output_dir 17_track_visualization/patient \
--rgb 016,085,154

# Filtered Proteins
gtfToGenePred 13_protein_filter/patient/Pat_with_cds_filtered.gtf 17_track_visualization/patient/Pat_filtered_proteins.genePred
genePredToBed 17_track_visualization/patient/Pat_filtered_proteins.genePred 17_track_visualization/patient/Pat_filtered_proteins.bed12

python ./00_scripts/17_add_rgb_to_bed.py \
--input_bed 17_track_visualization/patient/Pat_filtered_proteins.bed12 \
--output_dir 17_track_visualization/patient \
--rgb 016,085,154
```

## 18 - SUPPA 
```
module purge
module load gcc/11.4.0  
module load openmpi/4.1.4
module load python/3.11.4
module load miniforge/24.3.0-py3.11

conda create -n suppa

conda activate suppa

# Generate splicing events
python /project/sheynkman/programs/SUPPA-2.4/suppa.py generateEvents -i /project/sheynkman/external_data/GENCODE_v46/gencode.v46.basic.annotation.gtf -o 18_SUPPA/events -f ioi

python /project/sheynkman/programs/SUPPA-2.4/suppa.py generateEvents -i 08_rename_cds_to_exon/mother/Mot.cds_renamed_exon.gtf -o 18_SUPPA/LRP_events/mother.events -e SE SS MX RI FL -f ioe

python /project/sheynkman/programs/SUPPA-2.4/suppa.py generateEvents -i 08_rename_cds_to_exon/patient/Pat.cds_renamed_exon.gtf -o 18_SUPPA/LRP_events/patient.events -e SE SS MX RI FL -f ioe

cd 18_SUPPA/LRP_events/

#Put all the ioe events in the same file:
awk '
    FNR==1 && NR!=1 { while (/^<header>/) getline; }
    1 {print}
' *.ioe > all.LRP.events.ioe

cd ../..

# create expression table
python 00_scripts/18_suppa_expression_table.py -f 17_track_visualization/mother/Mot_refined_cds.bed12 17_track_visualization/patient/Pat_refined_cds.bed12 -s sample1 sample2 -o 18_SUPPA/combined.cpm

# Calculate PSI values
python /project/sheynkman/programs/SUPPA-2.4/suppa.py psiPerEvent --ioe-file 18_SUPPA/LRP_events/all.LRP.events.ioe --expression-file 18_SUPPA/combined.cpm -o 18_SUPPA/combined_local

# Analyze differential splicing
python /project/sheynkman/programs/SUPPA-2.4/suppa.py diffSplice --method empirical --input 18_SUPPA/LRP_events/all.LRP.events.ioe --psi 18_SUPPA/combined_local.psi --tpm 18_SUPPA/combined.cpm --area 1000 --lower-bound 0.05 -gc -o 18_SUPPA/diff_splice_events

conda deactivate
```
## 19 - LRP Summary
First, we have to create fractional abundance tables for the mother and patient samples. Then, we will create a summary table. <br />
```
conda activate reference_tab

python 00_scripts/19_fractional_abundance.py 17_track_visualization/mother/Mot_refined_cds.bed12 17_track_visualization/patient/Pat_refined_cds.bed12 19_LRP_summary/19_transcript_expression_fractional_abundance.csv
```
Create summary tables for transcripts and SUPPA events. <br />
```
python 00_scripts/19_transcript_summary_interm.py
python 00_scripts/19_suppa_summary_interm.py
```
Create a mapping file to map splice events to transcripts and combine information for summary table. <br />
```
python 00_scripts/19_suppa_plus_transcript.py
```

