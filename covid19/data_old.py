"""Access data from json files as documents (paragraph level dicts)"""

# ---[ list ]-------------------------------------------------------------------

import os

def list_data_files():
	"""iterate over paths of all data files"""
	for dirpath,_,filenames in os.walk('data'):
		filenames = [f for f in filenames if f.endswith('.json')]
		if not filenames: continue
		for f in filenames:
			yield os.path.join(dirpath,f)

# ---[ convert ]----------------------------------------------------------------

import json

def json_to_docs(path):
	"""iterate over paragraph level documents from one json document"""
	paper = json.load(open(path,'rb'))
	# parts
	text_id = 0
	for part in ['abstract','body_text']:
		if part not in paper: continue
		for x in paper[part]:
			doc = {}
			# metadata
			doc['paper_id'] = paper['paper_id']
			doc['paper_title'] = paper['metadata']['title']
			doc['path'] = path
			doc['part'] = part
			text_id += 1
			doc['text_id'] = text_id
			#
			doc['text'] = x['text']
			doc['section'] = x['section']
			# bib
			doc['bib_titles'] = []
			for ref in x['cite_spans']:
				ref_id = ref['ref_id']
				if not ref_id: continue 
				ref_title = paper['bib_entries'][ref_id]['title'] # ERROR
				doc['bib_titles'] += [ref_title]
			# ref (tables and figures)
			doc['tables'] = []
			doc['figures'] = []
			for ref in x['ref_spans']:
				ref_id = ref['ref_id']
				if not ref_id: continue
				r = paper['ref_entries'][ref_id] # ERROR
				if r['type']=='table':
					doc['tables'] += [r['text']]
				if r['type']=='figure':
					doc['figures'] += [r['text']]
			yield doc

def doc_iter(limit=None):
	"""iterate over all documents (doc = single paragraph)"""
	from itertools import islice
	for path in islice(list_data_files(),limit):
		yield from json_to_docs(path)

def get_doc(path,text_id):
	"""get single document (paragraph)"""
	docs = json_to_docs(path)
	for doc in docs:
		if doc['text_id']==text_id:
			return doc

def get_doc_by_meta(meta):
	path = meta['path']
	text_id = meta['text_id']
	return get_doc(path,text_id)

# ------------------------------------------------------------------------------

if __name__=="__main__":
	from pprint import pprint
	from itertools import islice
	from collections import Counter
	import csv
	cnt = Counter()
	empty = 0
	all = 0
	with open('data/metadata.csv','r',encoding='utf8') as csv_f:
		reader = csv.DictReader(csv_f)
		for row in islice(reader,None):
			if row['sha']=='':
				empty += 1
			else:
				key = hash(row['title'])
				cnt[key] += 1
			all += 1
		print(empty,all)
	pprint(cnt.most_common(30))
	print(sum([1 if c>1 else 0 for h,c in cnt.items()]))
	print(sum([c if c>1 else 0 for h,c in cnt.items()]))
	exit()
	from tqdm import tqdm
	cnt = {}
	files = tqdm(list_data_files())
	for path in files:
		doc = json.load(open(path,'rb'))
		t = doc['metadata']['title']
		if t not in cnt:
			cnt[t] = [path]
		else:
			cnt[t] += [path]
	by_cnt = list(cnt.items())
	by_cnt.sort(key=lambda x:len(x[1]),reverse=True)
	pprint(by_cnt[:10])
