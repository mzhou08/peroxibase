from lxml import html
import requests

import os
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile

source_file= open("./RedOxiBase_Bacteroidetes_Chlorobi_fasta.txt", "r")
lines = source_file.readlines()
## fasta format 
## >ID|NAME|...
## SEQUENCE VALUE
## empty line
line_count = 1
not_found_count = 0
found_count = 0
print(f"""sequence name\tuniprot id\tmodDB id""")
for line in lines:
    if line_count % 3 == 1:
        # init
        sequence_name = "" 
        uniprot_id = ""
        protein_id = ""

        line = line[1:]

        # then split to list
        line_list = line.split("|")

        # the second item in the list is the sequence name
        sequence_name = line_list[1]

        #print(sequence_name)

        # use the sequence name to query UniProtKB
        page_string = ""
        page = requests.get(f"""https://www.uniprot.org/uniprot/?query={sequence_name}&sort=score""")
        page_string = page.content
        if "Sorry, no results found for your search term" in str(page_string):
            not_found_count = not_found_count + 1
            #print(f"""Cannot find {sequence_name} in UniProtKB. """)
        else:
            found_count = found_count + 1
            tree = html.fromstring(page_string)
            #print(page_string)
            #This will get uniprot_id
            uniprot_id_list = tree.xpath("//a[starts-with(@href, '/uniprot/') and not (starts-with(@href, '/uniprot/?'))]/text()")
            uniprot_id=uniprot_id_list[0]
            #print(uniprot_id)
            #print(f"""https://modbase.compbio.ucsf.edu/modbase-cgi/model_search.cgi?searchkw=name&kword={uniprot_id}""")

            # use the uniprot_id to query uniprot
            modbase_page = requests.get(f"""https://modbase.compbio.ucsf.edu/modbase-cgi/model_search.cgi?searchmode=default&displaymode=moddetail&searchproperties=database_id&searchvalue={uniprot_id}&organism=ALL&organismtext=""")
            
            if modbase_page.history:
                ##print("Request was redirected")
                ##for resp in modbase_page.history:
                    ##print(f"""{resp.status_code}    {resp.url}""")
                ##print("Final destination:")
                #print(modbase_page.status_code, modbase_page.url)
                final_modbase_page = requests.get(f"""{modbase_page.url}""")
            else:
                ##print("Request was not redirected")
                final_modbase_page = modbase_page

            modbase_page_tree=html.fromstring(final_modbase_page.content)

            protein_id_list=modbase_page_tree.xpath("//a[starts-with(@href, 'http://www.rcsb.org/pdb/explore/explore.do?structureId=')]/text()")
            if len(protein_id_list) > 0:
                protein_id = protein_id_list[0]
                #print(f"""found protein_id {protein_id}""")
            #else:
                #print("no protein found")
            
        print(f"""{sequence_name}\t{uniprot_id}\t{protein_id}""")
    line_count = line_count + 1

#print(f"""not found {not_found_count}""")
#print(f"""found {found_count}""")



