#python extract_rows.py file1.txt file2.txt output.txt
#这个脚本将读取 file1.txt 和 file2.txt，然后找出 file1.txt 中的内容在 file2.txt 中第二列对应的行，并将这些行写入到 output.txt。
import sys

def read_file(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]

def write_file(file_path, lines):
    with open(file_path, 'w') as file:
        for line in lines:
            file.write(line + '\n')

def main(input_file1, input_file2, output_file):
    # Read file1 and file2
    file1_content = read_file(input_file1)
    file2_content = read_file(input_file2)

    # Extract matching lines
    matching_lines = [line for line in file2_content if len(line.split()) > 1 and line.split()[1] in file1_content]

    # Write matching lines to the output file
    write_file(output_file, matching_lines)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py <input_file1> <input_file2> <output_file>")
        sys.exit(1)

    input_file1 = sys.argv[1]
    input_file2 = sys.argv[2]
    output_file = sys.argv[3]

    main(input_file1, input_file2, output_file)
