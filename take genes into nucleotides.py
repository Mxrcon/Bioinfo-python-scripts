
from Bio import SeqIO
import sys
import os
#Determinando os inputs e outputs
entrada = sys.argv[1]
saida = sys.argv[2]
Lista = ["recA","rpoB"]
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
	for seq_record in SeqIO.parse(entrada+"/"+i , 'genbank'):
		for feature in seq_record.features:
			if feature.type == "CDS" and "gene" in feature.qualifiers:
				gene = feature.qualifiers['gene'][0]
				if gene in Lista:
					if not os.path.exists(saida+"/"+gene):
    						os.makedirs(saida+"/"+gene)
					with open(saida+"/"+gene+"/"+seq_record.id+".fasta", "w") as ofile:
						ofile.write(">{0}\n{1}\n".format(seq_record.id, feature.location.extract(seq_record).seq))



