import pandas as pd

# Load your existing summary table
summary_table_path = '19_LRP_summary/19_transcript_expression_fractional_abundance.csv'  # Update path as needed
summary_table = pd.read_csv(summary_table_path, sep=",")  # Use the appropriate delimiter

# Ensure relevant columns are present
required_columns = ['gene_name', 'pb_id', 'cpm_mother', 'cpm_patient']
missing_columns = [col for col in required_columns if col not in summary_table.columns]
if missing_columns:
    raise ValueError(f"Missing columns in summary table: {missing_columns}")

# Rename columns for clarity
summary_table.rename(columns={
    'gene_name': 'Gene',
    'pb_id': 'Transcript',
    'cpm_mother': 'mother_cpm',
    'cpm_patient': 'patient_cpm'
}, inplace=True)

# Calculate delta_cpm
summary_table['delta_cpm'] = summary_table['patient_cpm'] - summary_table['mother_cpm']

# Select the desired columns
transcript_cpm = summary_table[['Gene', 'Transcript', 'mother_cpm', 'patient_cpm', 'delta_cpm']]

# Save to tab-delimited file
transcript_cpm.to_csv('19_LRP_summary/19_transcript_cpm.csv', index=False, sep="\t")  # Save as tab-delimited

print("transcript_cpm.csv has been created successfully.")
