import pandas as pd

# Load the transformed SUPPA output and the transcript CPM data
transformed_suppa_path = '19_LRP_summary/19_transformed_suppa_output.csv'  # Update the path as needed
transcript_cpm_path = '19_LRP_summary/19_transcript_cpm.csv'  # Update the path as needed

transformed_suppa_data = pd.read_csv(transformed_suppa_path, sep="\t")
transcript_cpm_data = pd.read_csv(transcript_cpm_path, sep="\t")

# Check the first few rows of each DataFrame for verification
print("Transformed SUPPA data:")
print(transformed_suppa_data.head())
print("\nTranscript CPM data:")
print(transcript_cpm_data.head())

# Split the 'Alternative_splice' column to get individual gene names
transformed_suppa_data['Gene'] = transformed_suppa_data['Alternative_splice'].str.split(';').str[0]

# Merge the two DataFrames on the 'Gene' column to map SUPPA events to gene names
merged_data = pd.merge(transcript_cpm_data, transformed_suppa_data, on='Gene', how='left')

# Rename columns for clarity
merged_data = merged_data.rename(columns={
    'mother_cpm': 'mother_cpm', 
    'patient_cpm': 'patient_cpm', 
    'mother_psi': 'mother_psi', 
    'patient_psi': 'patient_psi'
})

# Calculate delta_cpm if not already in the data
merged_data['delta_cpm'] = merged_data['patient_cpm'] - merged_data['mother_cpm']

# Format the delta_cpm column to 5 decimal places
merged_data['delta_cpm'] = merged_data['delta_cpm'].round(5)

# Select the desired columns for output
output_columns = [
    'Gene', 
    'Transcript', 
    'mother_cpm', 
    'patient_cpm', 
    'delta_cpm', 
    'Alternative_splice', 
    'mother_psi', 
    'patient_psi', 
    'delta_psi'
]
final_data = merged_data[output_columns]

# Save the combined data to a new file
final_data.to_csv('19_LRP_summary/19_AS_transcript_combined.csv', index=False, sep="\t")  # Save as tab-delimited

print("AS_transcript_combined.csv has been created successfully.")
