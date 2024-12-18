import pandas as pd

# Load the SUPPA output
suppa_file_path = '18_SUPPA/diff_splice_events.psivec'  # Update the path as needed
suppa_data = pd.read_csv(suppa_file_path, sep="\t")  # Assuming the input is tab-delimited

# Check for required columns
required_columns = ['Alternative_splice', 'combined_local_1', 'combined_local_2']
missing_columns = [col for col in required_columns if col not in suppa_data.columns]
if missing_columns:
    raise ValueError(f"Missing columns in SUPPA data: {missing_columns}")

# Rename columns for clarity
suppa_data.rename(columns={
    'combined_local_1': 'mother_psi',
    'combined_local_2': 'patient_psi'
}, inplace=True)

# Calculate delta_psi
suppa_data['delta_psi'] = suppa_data['patient_psi'] - suppa_data['mother_psi']

# Select the desired columns
transformed_data = suppa_data[['Alternative_splice', 'mother_psi', 'patient_psi', 'delta_psi']]

# Save the transformed data to a new file
transformed_data.to_csv('19_LRP_summary/19_transformed_suppa_output.csv', index=False, sep="\t")  # Save as tab-delimited

print("transformed_suppa_output.csv has been created successfully.")
