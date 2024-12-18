import pandas as pd

# Paths to GTF files
mother_gtf_path = '07_make_cds_gtf/mother/Mot_cds.gtf'  # Update with actual file path
patient_gtf_path = '07_make_cds_gtf/patient/Pat_cds_updated.gtf'  # Update with actual file path

# Function to extract CPM from GTF file, ensuring each transcript per gene is retained
def extract_cpm_from_gtf(gtf_path):
    data = {}
    with open(gtf_path, 'r') as file:
        for line in file:
            if line.strip() and not line.startswith('#'):
                fields = line.strip().split('\t')
                if fields[2] == 'exon':  # Only consider exons
                    gene_info = fields[8]
                    # Extract gene name and transcript info from attributes
                    gene_name = gene_info.split('gene_id "')[1].split('";')[0]
                    transcript_info = gene_info.split('transcript_id "')[1].split('";')[0]
                    
                    # Split the transcript info to get transcript ID and CPM
                    parts = transcript_info.split('|')
                    if len(parts) == 3:
                        transcript_id = parts[1]
                        cpm_value = float(parts[2])  # Convert CPM to float
                        
                        # Store only the first CPM occurrence per unique (gene_name, transcript_id)
                        if (gene_name, transcript_id) not in data:
                            data[(gene_name, transcript_id)] = cpm_value

    # Convert dictionary to DataFrame, retaining each unique transcript per gene
    df = pd.DataFrame([(k[0], k[1], v) for k, v in data.items()], columns=['Gene', 'Transcript', 'CPM'])
    return df

# Extract CPM data from mother and patient GTF files
mother_cpm_df = extract_cpm_from_gtf(mother_gtf_path).rename(columns={'CPM': 'mother_cpm'})
patient_cpm_df = extract_cpm_from_gtf(patient_gtf_path).rename(columns={'CPM': 'patient_cpm'})

# Merge data on Gene and Transcript to align mother and patient CPM values
cpm_df = pd.merge(mother_cpm_df, patient_cpm_df, on=['Gene', 'Transcript'], how='outer')

# Calculate delta_cpm
cpm_df['delta_cpm'] = cpm_df['patient_cpm'] - cpm_df['mother_cpm']

# Format delta_cpm to 5 decimal places
cpm_df['delta_cpm'] = cpm_df['delta_cpm'].round(5)

# Save final table to a tab-delimited file
output_path = '19_LRP_summary/19_transcript_cpm.csv'
cpm_df.to_csv(output_path, index=False, sep="\t")

print("transcript_cpm.csv has been created successfully.")
