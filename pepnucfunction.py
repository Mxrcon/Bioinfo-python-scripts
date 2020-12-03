from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
import sys
import progressbar as pb
import os

"""
Developed by Davi J. Marcon Github: Mxrcon
E-mail:davijosuemarcon@gmail.com
Requirements: Biopython and progressbar packages 
Python script for generate .pep, .nuc and .function files for pgap input
usage: script.py [1] [2]
where: [1] = input folder containing .gbk files and [2] = output folder where resulting files will be created


"""
class progress_timer:
	def __init__(self, n_iter, description=""):
		self.n_iter = n_iter
		self.iter = 0
		self.description = description+":"
		self.timer = None
		self.initialize()
	def initialize(self):
		widgets= [self.description,pb.Percentage(),"",pb.Bar(marker=pb.RotatingMarker()),"",pb.ETA()]
		self.timer= pb.ProgressBar(widgets=widgets,maxval=self.n_iter).start()
	def update(self,q=1):
		self.timer.update(self.iter)
		self.iter += q
	def finish(self):
		self.timer.finish()






class sequence:
	def __init__(self,seq_id,seq,seq_product,seq_translation,cog):
		self.id = seq_id
		self.seq = seq
		self.product =seq_product
		self.translation = seq_translation
		self.cog = cog

def pep(sequence_list,output_folder,name):
	records = [SeqRecord(Seq(seq.translation,),id=seq.id,description="",) for seq in sequence_list]
	SeqIO.write(records,output_folder+"/"+name+".pep","fasta")

def nuc(sequence_list,output_folder,name):
	records = [SeqRecord(seq.seq,id=seq.id,description="",) for seq in sequence_list]
	SeqIO.write(records,output_folder+"/"+name+".nuc","fasta")

def func(sequence_list,output_folder,name):
	function = [seq.id+"\t"+seq.cog+"\t"+seq.product+"\n" for seq in sequence_list]
	function = "".join(function)
	with open(output_folder+"/"+name+".function",'w') as output:
		output.write(function)
		output.close()

def open_gbk(seq_file):
	sequence_list,id_list = [],[]
	for seq_record in SeqIO.parse(seq_file , 'genbank'):
		genome = seq_record.seq
		for feature in seq_record.features:
			if feature.type == "CDS":
				gene = feature
				feature_id = feature.qualifiers['locus_tag'][0]
				feature_product = feature.qualifiers['product'][0]
				feature_translation = feature.qualifiers['translation'][0]
				if feature.location.strand == 1:
					feature_sequence = genome[feature.location.start:feature.location.end]
				if feature.location.strand == -1:
					feature_sequence = genome[feature.location.start:feature.location.end].reverse_complement()
				try:
					if feature.qualifiers['db_xref'][0].split(":")[0] == "COG":
						feature_cog = feature.qualifiers['db_xref'][0].split(":")[1]
				except:
					feature_cog = "-" 
				sequence_list.append(sequence(feature_id,feature_sequence,feature_product,feature_translation,feature_cog))

	return sequence_list		

def file_handler(input_file,output_folder):
	name = input_file.split(".gb")[0].split("/")[1]
	sequence_list = open_gbk(input_file)
	pep(sequence_list,output_folder,name)
	nuc(sequence_list,output_folder,name)
	func(sequence_list,output_folder,name)		
#Inputs and outputs
input_folder = sys.argv[1]
output_folder= sys.argv[2]
#Output check
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
#Running code
pt= progress_timer(description="Running",n_iter=len(os.listdir(input_folder)))
for i in os.listdir(input_folder):
	pt.update()
	open(input_folder+"/"+i,"r")
	file_handler(input_folder+"/"+i, output_folder)
pt.finish()
print("Done!")



