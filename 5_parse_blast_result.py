import pandas as pd

# df is a pandas.DataFrame and blast-out.b6 won't have a header
df = pd.read_table('./result_3_output.csv')

# the default outfmt 6 columns
#default_outfmt6_cols = 'qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore'.strip().split(' ')
#df.columns = default_outfmt6_cols
new= df.groupby(['qseqid', 'sseqid']).apply(lambda x: x.nlargest(1,['bitscore'])).reset_index(drop=True)

new_sorted_df= new.sort_values(by=['qseqid', 'sseqid'], ascending=False)
print("sss")
print(new_sorted_df)

## get the original sequence dataframe
original_df = pd.read_csv('./result_1_fasta.csv', header=0)
original_df['qseqid']=original_df['Id'].map(str) + "|" + original_df['Name'] + "|"

print(original_df)

new_df = pd.merge(new_sorted_df, original_df,  how='left', on='qseqid')
print(new_df)
new_df.to_csv(r'result_5_all.csv',index=False)


## find out catalase class
#new_df_catalase_peroxidase = new_df.loc[new_df["Class"] == "Catalase peroxidase"]
#new_df_catalase_peroxidase.to_csv(r'result_5_catalase_peroxidase.csv',index=False)

#new_df_catalase = new_df.loc[new_df["Class"] == "Catalase"]
#new_df_catalase.to_csv(r'result_5_catalase.csv',index=False)


# filter for pident >= 30 and evalue <= 0.001
#df_filtered = df[(df['pident'] >= 30.0) & (df['evalue'] <= 0.001)]

# df_filtered contains only hits with >= 99.0% identity and e-value <= 0.001

# sort by bitscore
#df_filtered_sorted=df_filtered.sort_values(by='bitscore', ascending=False)

# df_filtered is now sorted by bitscore in descending order
#print(df_filtered)