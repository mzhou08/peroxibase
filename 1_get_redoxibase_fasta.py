from lxml import html
import requests

import os
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile

df = pd.read_excel('./RedOxiBase_Bacteroidetes_Chlorobi.xlsx', sheet_name='Sheet1')
# add new column
df["Fasta"] = ""

# prepare to output new csv file with fasta info
os.remove("fasta.csv")
for index, row in df.iterrows():
    id = row["Id"]
    df.at[index, "Name"]=row["Name"].strip()
    page = requests.get(f"""http://peroxibase.toulouse.inra.fr/tools/get_fasta/{id}/PEP""")
    tree = html.fromstring(page.content)

    #This will get fasta
    fasta = tree.xpath('//textarea[@name="task_data_input"]/text()')
    print(fasta)
    df.at[index, "Fasta"] = fasta

df.to_csv(r'fasta.csv',index=False)