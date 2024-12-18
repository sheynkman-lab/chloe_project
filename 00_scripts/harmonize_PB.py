# Paths to the GTF files
mother_gtf_path = '07_make_cds_gtf/mother/Mot_cds.gtf'  # Update with actual file path
patient_gtf_path = '07_make_cds_gtf/patient/Pat_cds.gtf'  # Update with actual file path
output_patient_gtf_path = '07_make_cds_gtf/patient/Pat_cds_updated.gtf'  # Output path for modified patient GTF

# Function to create a mapping from mother GTF based on coordinates
def create_mapping_from_mother_gtf(gtf_path):
    accession_mapping = {}
    with open(gtf_path, 'r') as file:
        for line in file:
            if line.strip() and not line.startswith('#'):
                fields = line.strip().split('\t')
                if fields[2] == 'exon' or fields[2] == 'CDS':
                    # Extract gene and transcript information
                    gene_info = fields[8]
                    transcript_info = gene_info.split('transcript_id "')[1].split('";')[0]
                    
                    # Create a key based on the coordinates
                    coord_key = (fields[0], int(fields[3]), int(fields[4]))  # (chromosome, start, end)
                    accession_mapping[coord_key] = transcript_info
    return accession_mapping

# Function to rename patient PB accessions based on matching coordinates
def rename_patient_accessions(patient_gtf_path, accession_mapping):
    patient_counter = 1
    modified_lines = []
    
    with open(patient_gtf_path, 'r') as file:
        for line in file:
            if line.strip() and not line.startswith('#'):
                fields = line.strip().split('\t')
                if fields[2] == 'exon' or fields[2] == 'CDS':
                    gene_info = fields[8]
                    transcript_info = gene_info.split('transcript_id "')[1].split('";')[0]
                    parts = transcript_info.split('|')
                    
                    # Extract the original CPM value
                    original_cpm = parts[-1]  # Assuming the CPM value is the last part of transcript_info
                    
                    # Create a key based on the coordinates
                    coord_key = (fields[0], int(fields[3]), int(fields[4]))  # (chromosome, start, end)
                    
                    # Check if the coordinates exist in the mapping
                    if coord_key in accession_mapping:
                        # Use the accession from the mother GTF
                        modified_transcript_info = accession_mapping[coord_key]
                    else:
                        # This is a patient transcript, name it accordingly
                        modified_transcript_info = f"{parts[0]}|PB.patient.{patient_counter}|{original_cpm}"
                        patient_counter += 1
                        
                    # Reconstruct the line with the modified transcript_id, keeping the original CPM value
                    new_gene_info = gene_info.replace(transcript_info, modified_transcript_info)
                    modified_lines.append(f"{fields[0]}\t{fields[1]}\t{fields[2]}\t{fields[3]}\t{fields[4]}\t{fields[5]}\t{fields[6]}\t{fields[7]}\t{new_gene_info}\n")
                else:
                    # Keep non-exon lines unchanged
                    modified_lines.append(line)

    return modified_lines

# Create accession mapping from the mother GTF based on coordinates
accession_mapping = create_mapping_from_mother_gtf(mother_gtf_path)

# Rename patient accessions and modify patient GTF
modified_patient_lines = rename_patient_accessions(patient_gtf_path, accession_mapping)

# Save the modified patient GTF
with open(output_patient_gtf_path, 'w') as output_file:
    output_file.writelines(modified_patient_lines)

print("Modified patient GTF file has been created successfully.")
