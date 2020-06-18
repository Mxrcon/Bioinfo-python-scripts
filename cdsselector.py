# -*- coding:utf-8 -*-
"""     O objetivo deste script é remover CDS não desejadas, 
	ao determinar quais as CDS que você deseja manter no
	GBK. Para isso devem ser utilizados arquivos GBK full
	devidamente anotados.
	
	python a.py 1 2 3
	1 = nome da pasta com os gbk input
	2 = nome da pasta para os outputs
	3 = nome da lista com os genes para serem mantidos
	OBS: A formatação dos genes deve ser mantida de forma
	simples, apenas uma sigla de gene por linha, que não 
	deve conter aspas ou espaço.	
	Desenvolvido por Davi J. Marcon
	Email: Davijosuemarcon@gmail.com
"""
from Bio import SeqIO
import sys
import os
#Determinando os inputs e outputs
entrada = sys.argv[1]
saida = sys.argv[2]
Lista = [line.rstrip('\n') for line in open(sys.argv[3])]
#abrindo os inputs
for i in os.listdir(entrada):
	open(entrada+"/"+i)
#conta o numero de gbs
list = os.listdir(entrada)
number_files = len(list)
print("Foram encontrados" , (number_files), "arquivos")
#cria  a pasta de outputs
if not os.path.exists(saida):
    os.makedirs(saida)
#Executando código
for i in os.listdir(entrada): 
	FEATURES = []
	for seq_record in SeqIO.parse(entrada+"/"+i , 'genbank'):
		for feature in seq_record.features:
			if feature.type == "CDS" and "gene" in feature.qualifiers:
				gene = feature.qualifiers['gene'][0]
				if gene in Lista:
					FEATURES.append(feature)
			if feature.type == "gene" and "gene" in feature.qualifiers:
				gene = feature.qualifiers['gene'][0]
				if gene in Lista:
					FEATURES.append(feature)
			if feature.type == "source" and "mol_type" in feature.qualifiers:
				if feature.qualifiers["mol_type"][0] == 'genomic DNA':
					FEATURES.append(feature)
			seq_record.features = FEATURES
	print("Gerando output para: "+i)
	SeqIO.write (seq_record, saida+"/"+i, 'genbank')
