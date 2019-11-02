from Bio.Blast import NCBIWWW
from Bio import SeqIO

from Bio.Blast import NCBIXML

import os, ssl
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and 
    getattr(ssl, '_create_unverified_context', None)): 
    ssl._create_default_https_context = ssl._create_unverified_context 

record = SeqIO.read("./2369.fasta", format="fasta")

print(record)

result_handle = NCBIWWW.qblast("blastp", "nt", record.seq, url_base='https://blast.ncbi.nlm.nih.gov/Blast.cgi', entrez_query="txid4932[ORGN]")

print("after")

with open("my_blast.xml", "w") as out_handle:
    out_handle.write(result_handle.read())
result_handle.close()

result_handle = open("my_blast.xml")
blast_records = NCBIXML.parse(result_handle)
E_VALUE_THRESH = 0.04
for blast_record in blast_records:
    for alignment in blast_record.alignments:
        for hsp in alignment.hsps:
            if hsp.expect < E_VALUE_THRESH:
                print("****Alignment****")
                print("sequence:", alignment.title)
                print("length:", alignment.length)
                print("e value:", hsp.expect)
                print(hsp.query[0:75] + "...")
                print(hsp.match[0:75] + "...")
                print(hsp.sbjct[0:75] + "...")