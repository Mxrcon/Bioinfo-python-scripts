from Bio.PDB.PDBParser import PDBParser
from Bio.PDB.PDBList import PDBList

pdbl = PDBList()
parser = PDBParser()

for i in ["ID"]:
    pdbl.retrieve_pdb_file(pdb_code=i,file_format="pdb",pdir="./")
    structure_id = i
    filename = "pdb"+i.lower()+".ent"
    structure = parser.get_structure(structure_id, filename)
    print("id: ",structure_id)
    print("name: ", structure.header["name"])
    print("deposition date :", structure.header["deposition_date"])
    print("release date :", structure.header["release_date"])
    print("structure method : ", structure.header["structure_method"])
    print("resolution : ", structure.header["resolution"]) 
    print("")
