import os
import sys

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    # Use tab to split each line and return the second column
    return [line.strip().split('\t')[1] for line in lines if len(line.strip().split('\t')) > 1]  # Ensure enough columns

def extract_data(file1_path, file2_path, output_dir):
    file1_data = read_file(file1_path)
    with open(file2_path, 'r', encoding='utf-8') as file:
        file2_data = file.readlines()

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    for item in file1_data:
        for line in file2_data:
            columns = line.strip().split('\t')  # Split columns by tab
            if len(columns) > 11 and item in columns[11]:  # Check if item is in the 12th column
                output_file_path = os.path.join(output_dir, f"{item}.txt")
                with open(output_file_path, 'a', encoding='utf-8') as output_file:
                    if len(columns) > 2:  # Ensure there are at least 3 columns
                        output_file.write(columns[2] + '\n')  # Write the 3rd column to the file

# Check if enough command-line arguments are provided
if len(sys.argv) != 4:
    print("Usage: python script_name.py file1_path file2_path output_dir")
    sys.exit(1)

# Get file paths and output directory from command-line arguments
file1_path = sys.argv[1]
file2_path = sys.argv[2]
output_dir = sys.argv[3]

# Extract data and save to files
extract_data(file1_path, file2_path, output_dir)
