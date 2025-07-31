#python script.py input.txt output.txt
import sys

def extract_second_column(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        for line in infile:
            columns = line.split()
            if len(columns) >= 2:
                outfile.write(columns[1] + '\n')

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py input_file output_file")
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        extract_second_column(input_file, output_file)
