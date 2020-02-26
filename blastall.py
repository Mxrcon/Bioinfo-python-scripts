#
# -*- coding:utf-8 -*-
"""     Script com o proposito de realizar um blast usando varias querys e varias db
	as databases não precisam estar formatadas, apenas precisam estar no formato
	fasta. os resultados serão gerados automáticamente no formato de output 8
	sem nenhum comentário
	argumento 1 = pasta das querys
 	argumento 2 = pasta das databases
	argumento 3 = database type (nucl, prot) 
	argumento 3 = blast type (blastn, blastp,blastx) 
	argumento 4 = e-value 
"""
import sys
import os
import re
import time
from Bio.Blast.Applications import NcbiblastxCommandline
from Bio.Blast.Applications import NcbimakeblastdbCommandline
#time
start_time = time.time()

#determining arguments

query = sys.argv[1]
database_folder = sys.argv[2]
database_type = sys.argv[3]
blast_type = sys.argv[4]
output_format = 6
evalue_number = sys.argv[5]
if sys.argv[3] == "nucl":
	tipo = "nucleotideo"
if sys.argv[3] == "prot":
	tipo = "proteina" 

#printing status

print("Realizando: ", blast_type)
print("Inputs na pasta: ", query)
print("Database na pasta: ", database_folder)
print("Formato da database: ", tipo)
print("Formato do output: ", output_format)


#opening inputs
for i in os.listdir(query):
	open(query+"/"+i)
for i in os.listdir(database_folder):
	open(database_folder+"/"+i)


#conta o numero de fastas
lista1 = os.listdir(query)
number_query = len(lista1)
print("Foram encontrados" , (number_query), "querys")

#conta o numero de dbs
lista2 = os.listdir(database_folder)
number_db = len(lista2)
print("Foram encontrados" , (number_db), "databases")
#abre as dbs ignorando as ja criadas


#cria  a pasta de outputs
if not os.path.exists('outputs'):
    os.makedirs('outputs')

#formatando as databases
databasefiles = []
for i in os.listdir(database_folder):
	if not re.search('\S*\.(nin|nhr|nsq)',database_folder+"/"+i):
		Makedb = NcbimakeblastdbCommandline(dbtype=database_type, input_file=database_folder+"/"+i)
		Makedb()
		databasefiles.append(i)
print(number_db, "Databases formatadas no formato: ",tipo)

#definir o blast e executar
counter = 0
for i in os.listdir(query):
	counter = counter+1
	print ("analisandoquery: ("+str(counter)+"/"+str(number_query)+")") 
	for db in databasefiles:
		Blast = NcbiblastxCommandline(cmd=blast_type, query= query+"/"+i, db= database_folder+"/"+db, evalue=evalue_number, outfmt=output_format, out="outputs/"+i+"_"+db+"_result.txt")
		Blast()


#conta o numero de resultados
contador = number_query*number_db
print("Foram gerados" , contador, "arquivos de resultado")
print("Utilizando ", number_query, " querys e ", number_db,"databases")
tempofinal = (time.time() - start_time)
print("tempo para execucao:" "%s segundos " % (tempofinal))
