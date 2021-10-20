#!/usr/bin/env python3

from Bio import SeqIO
from Bio.Blast import NCBIWWW
import sys

input_file = sys.argv[1]
input_name = input_file.split(".")[0]

records = SeqIO.parse(input_file,"abi")
count = SeqIO.write(records, input_name+".fastq", "fastq")
print("Converted %i records" % count)
input_name = "teste"
# h37rv 16s portion
# fasta_string = "ggaattcctggtgtagcggtggaatgcgcagatatcaggaggaacaccggtggcgaaggcgggtctctgggcagtaactgacgctgaggagcgaaagcgtggggagcgaacaggattagataccctggtagtccacgccgtaaacggtgggtactaggtgtgggtttccttccttgggat"
fasta_string = open(input_name+".fasta").read()
result_handle = NCBIWWW.qblast("blastn", "nt", fasta_string, format_type="Text")

with open(input_name+"_blast_result.txt", "w") as out_handle:
     out_handle.write(result_handle.read())
     result_handle.close()

