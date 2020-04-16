import pandas as pd
from itertools import islice
import pickle
import re
from time import time
t0 = time()

df = pd.read_csv('metadata.csv')
print('columns',list(df))
selected = df[['cord_uid','sha','publish_time','journal','url','title']].where(df['sha'].notna())

meta_by_sha = {}

rows = selected.iterrows()
for _,r in rows:
	if type(r['cord_uid']) is float: continue # NaN
	for sha in r['sha'].split(';'):
		sha = sha.strip()
		if not re.match('^[a-f0-9]+$',sha):
			print(r)
			exit()
		meta = {k:r[k] for k in ['cord_uid','publish_time','journal','title']} 
		meta_by_sha[sha] = meta

pickle.dump(meta_by_sha,open('paper_meta_by_sha.pkl','wb'))
print(f"done in {time()-t0:.01f} seconds")
