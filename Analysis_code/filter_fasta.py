#python filter_fasta.py input.fasta filtered.fasta 300

import argparse
from Bio import SeqIO

def filter_fasta(input_file, output_file, min_length):
    with open(input_file, "r") as infile, open(output_file, "w") as outfile:
        for record in SeqIO.parse(infile, "fasta"):
            if len(record.seq) >= min_length:
                SeqIO.write(record, outfile, "fasta")

def main():
    parser = argparse.ArgumentParser(description="Filter sequences from a FASTA file by minimum length")
    parser.add_argument("input_file", help="Input FASTA file")
    parser.add_argument("output_file", help="Output FASTA file")
    parser.add_argument("min_length", type=int, help="Minimum sequence length to keep")

    args = parser.parse_args()

    filter_fasta(args.input_file, args.output_file, args.min_length)

if __name__ == "__main__":
    main()
