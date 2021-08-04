# silly script for writing mutations from 2 proteins in a pretty way
# doens't work with indels

original = "QEHDG"
engenheirada = "ARNDG"


aminoacid_dict = {"A":"Ala",
"R":"Arg",
"N":"Asn",
"D":"Asp",
"C":"Cys",
"Q":"Gln",
"E":"Glu",
"G":"Gly",
"H":"His",
"I":"Ile",
"L":"Leu",
"K":"Lys",
"M":"Met",
"F":"Phe",
"P":"Pro",
"O":"Pyl",
"S":"Ser",
"U":"Sec",
"T":"Thr",
"W":"Trp",
"Y":"Tyr",
"V":"Val",
"B":"Asx",
"Z":"Glx",
"X":"Xaa",
"J":"Xle"}

for i in range(0, len(original)):
    if original[i] != engenheirada[i]:
        print(aminoacid_dict[original[i]]+str(i+1)+aminoacid_dict[engenheirada[i]])
