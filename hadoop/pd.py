import pandas as pd

def get_meta(tsv_path):
	meta={}
	meta['names']=[]
	with open(tsv_path+'.meta','r') as f:
		for line in f:
			if not line.strip(): break
			col = line.rstrip().split('\t')
			meta['names'] += [col[0]]
	return meta

def df_from_csv(tsv_path, names=None, **kwargs):
	meta = get_meta(tsv_path)
	col_names = meta['names'] if not names else names
	df = pd.read_csv(tsv_path, header=None, names=col_names, **kwargs)
	return df

df = df_from_csv('data/test1.tsv',sep='\t')
print(df)
