import os
import sys
from Bio import SeqIO

def read_fasta_file(file_path):
    seq_records = []
    with open(file_path, 'r') as fasta_file:
        for record in SeqIO.parse(fasta_file, 'fasta'):
            seq_records.append(record)
    return seq_records

def extract_sequences_by_ids(fasta_file_path, id_file_path):
    sequences = read_fasta_file(fasta_file_path)
    id_set = set()
    with open(id_file_path, 'r') as id_file:
        for line in id_file:
            id_set.add(line.strip())

    extracted_sequences = []
    for seq_record in sequences:
        if seq_record.id in id_set:
            extracted_sequences.append(seq_record)

    return extracted_sequences

def write_sequences_to_fasta(extracted_sequences, output_folder, file_name):
    output_file_path = os.path.join(output_folder, file_name)
    os.makedirs(output_folder, exist_ok=True)  # 创建输出文件夹（如果不存在）
    with open(output_file_path, 'w') as output_file:
        SeqIO.write(extracted_sequences, output_file, 'fasta')

def process_id_files(input_folder, fasta_file_path, output_folder):
    for file_name in os.listdir(input_folder):
        if file_name.endswith('.txt'):
            id_file_path = os.path.join(input_folder, file_name)
            extracted_sequences = extract_sequences_by_ids(fasta_file_path, id_file_path)
            output_file_name = os.path.splitext(file_name)[0] + '.fasta'
            write_sequences_to_fasta(extracted_sequences, output_folder, output_file_name)

# 从命令行获取参数
if len(sys.argv) != 4:
    print("Usage: python script.py <input_folder> <fasta_file_path> <output_folder>")
    sys.exit(1)

input_folder = sys.argv[1]  # 输入文件夹路径
fasta_file_path = sys.argv[2]  # FASTA文件路径
output_folder = sys.argv[3]  # 输出文件夹路径

# 调用函数处理文件
process_id_files(input_folder, fasta_file_path, output_folder)