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
	def __init__(self,information_list,genome):
		if "complement" in information_list[0]:
			self.location = information_list[0].strip("     CDS             ").strip("complement(").strip(")").split("..")
			self.seq = Seq(genome[int(int(self.location[0])-1):int(int(self.location[1]))]).reverse_complement()
		if "complement" not in information_list[0]:
			self.location = information_list[0].strip("     CDS             ").strip("complement(").strip(")").split("..")
			self.seq = Seq(genome[int(int(self.location[0])-1):int(int(self.location[1]))])
		for i in information_list[0:3]:
			if i.split("=")[0].replace(" ","") == "/locus_tag":
				self.id = i.split("=")[1].strip("\"").replace(" ","")
		trans_location = []
		counter =0
		for i in information_list:
			if "translation" in i:
				trans_location.append(counter)
			if " gene" in i or "ORIGIN " in i:
				trans_location.append(counter)

			counter+=1
		self.translation = "".join(information_list[trans_location[0]:trans_location[1]]).replace("/translation=","").replace("\"","").replace(" ","")
		for i in information_list[2:-2]:
			if i.split("=")[0].replace(" ","") == "/product":
				self.product = i.split("=")[1].strip("\"")			
			self.cog = "-"
			if i.split("=")[0].replace(" ","") == "/db_xref":
				if i.split("=")[1].strip("\"").split(":")[0] == "COG":
 					self.cog = i.split("=")[1].strip("\"").split(":")[1]
			if self.cog != "-":
				break
def pep(sequence_list,output_folder,name):
	records = [SeqRecord(Seq(seq.translation),id=seq.id,description="",) for seq in sequence_list]
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





def open_gbk(file_input):
	file_input = open(file_input,"r")
	file_input = file_input.readlines()
	counter = 0
	information_location,cds_locations,genome_locations = [],[],[]
	for i in file_input:
		counter+=1
		if "CDS" in i.split(" "):
			cds_locations.append(file_input[counter-1].split(" ")[-1].strip().split(".."))
			information_location.append(counter-1)
		if i == "ORIGIN      \n":
			genome_locations.append(counter)
		if i == "//\n":
			genome_locations.append(counter)
	
	genome = "".join(file_input[genome_locations[0]:genome_locations[1]])
	filtered_genome = "".join(i.upper() for i in genome if i.isalpha())
	informations = []
	for i in range(len(information_location)):
		if information_location[i] == information_location[-1]:
			informations.append(file_input[information_location[i]:genome_locations[0]])
			break
		informations.append(file_input[information_location[i]:information_location[i+1]])
	filtered_informations = []
	for i in informations:
		filtered_i = []
		for o in i:
			filtered_i.append(o.strip("\n"))
		filtered_informations.append(filtered_i)
	
	sequence_list = [sequence(i,filtered_genome) for i in filtered_informations]
	return sequence_list

	
def file_handler(input_file,output_folder):
	name = input_file.split(".gb")[0].split("/")[1]
	sequence_list = open_gbk(input_file)
	pep(sequence_list,output_folder,name)
	nuc(sequence_list,output_folder,name)
	func(sequence_list,output_folder,name)

###EXECUTION

	
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


