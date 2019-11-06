from Bio.Blast.Applications import NcbiblastpCommandline
import pandas as pd
from io import StringIO
from Bio.Blast import NCBIXML
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio import SeqIO



df = pd.read_csv("./fasta.csv")
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
for index, row in df.iterrows():
    # init
    fasta_value = row["Fasta"]
    # Create two sequence files
    query_seq=SeqRecord(Seq(fasta_value),id="query_seq")
    SeqIO.write(query_seq, "query_seq.fasta", "fasta")

    # Run BLAST and parse the output as XML
    cline = NcbiblastpCommandline(query="query_seq.fasta", subject="yeast.fasta", outfmt=5)
    print(cline)
    output = cline()[0]
    blast_result_record = NCBIXML.read(StringIO(output))
    # Print some information on the result
    for alignment in blast_result_record.alignments:
        for hsp in alignment.hsps:
            print(f"""\n\n****{row['Name']} Alignment with yeast ****""")
            print('sequence:', alignment.title)
            print('length:', alignment.length)
            print('e value:', hsp.expect)
            print(hsp.query)
            print(hsp.match)
            print(hsp.sbjct)