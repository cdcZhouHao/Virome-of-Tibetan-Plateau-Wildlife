import sys

def read_file(file_path):
    with open(file_path, 'r') as file:
        return set(line.strip() for line in file)

def write_file(file_path, data):
    with open(file_path, 'w') as file:
        for item in data:
            file.write(f"{item}\n")

def main(file1_path, file2_path, output_file_path):
    set1 = read_file(file1_path)
    set2 = read_file(file2_path)
    
    diff = set2 - set1
    
    write_file(output_file_path, diff)
    print(f"Difference written to {output_file_path}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py <file1> <file2> <output_file>")
    else:
        file1_path = sys.argv[1]
        file2_path = sys.argv[2]
        output_file_path = sys.argv[3]
        main(file1_path, file2_path, output_file_path)
