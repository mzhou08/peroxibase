from lxml import html
import requests

import os
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile

df = pd.read_excel('RedOxiBase_Bacteroidetes_Chlorobi.xlsx', sheetname='Sheet1')

print(df.head(5))
ID_list = df["Id"].tolist()

print(ID_list)

print(len(ID_list))

os.remove("RedOxiBase_Bacteroidetes_Chlorobi_fasta.txt")
f= open("RedOxiBase_Bacteroidetes_Chlorobi_fasta.txt","w+")

for id in ID_list:   
    page = requests.get(f"""http://peroxibase.toulouse.inra.fr/tools/get_fasta/{id}/PEP""")
    print(page)
    tree = html.fromstring(page.content)

    #This will get fasta
    fasta = tree.xpath('//textarea[@name="task_data_input"]/text()')
    print(fasta)
    f.write(fasta[0])
f.close()