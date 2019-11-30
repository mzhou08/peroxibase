from Bio.Blast.Applications import NcbiblastpCommandline
import pandas as pd
from io import StringIO
from Bio.Blast import NCBIXML
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio import SeqIO



# output concatenated fasta values based ono peroxi class
# catalase class name
class_name = "Manganese Catalase"

df = pd.read_csv("./result_1_fasta.csv")
## fasta format 
## >ID|NAME|...
## SEQUENCE VALUE
## empty line
line_count = 1
not_found_count = 0
found_count = 0

# form the query string from peroxibase sequences
fasta_value=""
for index, row in df.iterrows():
    # filter by Class name
    if (row["Class"]) == class_name:
        print(row["Fasta"])
        fasta_value = fasta_value + "\n" + row["Fasta"]

output_file_name = f"""fasta_{class_name}.txt"""
f= open(output_file_name, "w+")
f.write(fasta_value)
f.close()