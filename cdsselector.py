# -*- coding:utf-8 -*-
"""    
	Propouse:
		This script removes CDS that arent on the allowed list, 
		with annoted GBK files you can create a GBK that only
		contains CDS that are ´allowed´ by the list.

	Usage:	
	python cdsselector.py $GBK_FOLDER $OUTDIR #LIST_FILE

	$GBK_FOLDER = Folder containing all gbk files that will be used as input

	$OUTDIR = Name of the output dir

	$LIST_FILE = A file containt a gene on every line following this example:
	dnaA
	dnaK
	rpoB

	OBS: the list file shouldn't contain and special character.
"""
from Bio import SeqIO
import sys
import os

#I/O declaration

input_folder = sys.argv[1]
output_folder = sys.argv[2]
gene_list = [line.strip('\n') for line in open(sys.argv[3])]

#Taking permission for parsing later
for i in os.listdir(input_folder):
	open(input_folder+"/"+i)

#Check output folder existance
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

#Code
for input_file in os.listdir(input_folder): 
	FEATURES = []
	for seq_record in SeqIO.parse(input_folder+"/"+input_file , 'genbank'):# Parse all files and interact around them
		for feature in seq_record.features: # Check each feature and see if it is on gene_list
			if feature.type == "CDS" and "gene" in feature.qualifiers:
				gene = feature.qualifiers['gene'][0]
				if gene in gene_list:
					FEATURES.append(feature)
			if feature.type == "gene" and "gene" in feature.qualifiers:
				gene = feature.qualifiers['gene'][0]
				if gene in gene_list:
					FEATURES.append(feature)
			if feature.type == "source" and "mol_type" in feature.qualifiers:
				if feature.qualifiers["mol_type"][0] == 'genomic DNA':
					FEATURES.append(feature)# If the feature is on the gene_list append them to the new feature list
			seq_record.features = FEATURES
	print("Creating input for: "+input_file)
	SeqIO.write (seq_record, output_folder+"/"+input_file, 'genbank')
