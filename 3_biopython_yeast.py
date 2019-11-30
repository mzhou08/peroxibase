from Bio.Blast.Applications import NcbiblastpCommandline
import pandas as pd
from io import StringIO
from Bio.Blast import NCBIXML
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio import SeqIO



df = pd.read_csv("./result_1_fasta.csv")
# add new column
df["uniprot_id"] = ""
df["protein_id"] = ""

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
    # init
    fasta_value = fasta_value + row["Fasta"]
print(fasta_value)

# Create two sequence files
#query_seq=SeqRecord(Seq(fasta_value),id="query_seq")
#SeqIO.write(query_seq, "peroxibase.fasta", "fasta")
f= open("peroxibase.fasta", "w+")
f.write(fasta_value)
f.close()

# Run BLAST and parse the output as XML
cline = NcbiblastpCommandline(query="peroxibase.fasta", subject="GCF_000146045.2_R64_protein.faa", 
                #outfmt='6 qseqid sseqid qstart qend evalue', 
                outfmt='6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore', 
                out="result_3_output.csv", evalue=1e-5)
print(cline)
output = cline()[0]
#blast_result_record = NCBIXML.read(StringIO(output))
print(StringIO(output))
# Print some information on the result
#for alignment in blast_result_record.alignments:
#    for hsp in alignment.hsps:
#        print(f"""\n\n****{row['Name']} Alignment with yeast ****""")
#        print('sequence:', alignment.title)
#        print('length:', alignment.length)
#        print('e value:', hsp.expect)
#        print(hsp.query)
#        print(hsp.match)
#        print(hsp.sbjct)