# -*- coding:utf-8 -*-
"""     Script com o proposito de renomear arquivos .fasta baixados do NCBI baseando-se na primeira linha

        argumento 1 = nome do arquivo
"""
#import
import sys
import os
#openfile
file = sys.argv[1]
fasta = [line.strip('\n') for line in open(file)]
name = fasta[0].split(" ")
X = name[1:len(name)]
y = []
for i in X:
	i = i.strip(",")
	i = i.replace('|','a')
	i = i.replace('_','-')
	i = i.replace('/','-')
	if i not in ["str.", "substr.", "complete", "genome","strain","chromosome","scaffold","whole","shotgun","sequence"]:
		y.append (i)
		fasta_name = "-".join(y)
os.popen("mv "+file+" "+fasta_name+".fasta")
print ("Done!")	
  	
