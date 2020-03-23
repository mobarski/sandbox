import os

# ---[ list ]-------------------------------------------------------------------

def list_data_files():
	for dirpath,_,filenames in os.walk('data'):
		filenames = [f for f in filenames if f.endswith('.json')]
		if not filenames: continue
		for f in filenames:
			yield os.path.join(dirpath,f)

# ---[ convert ]----------------------------------------------------------------

import json

def raw_to_records(path):
	"""iterate over records from one raw document"""
	rec = {}
	doc = json.load(open(path,'rb'))
	# metadata
	rec['paper_id'] = doc['paper_id']
	rec['paper_title'] = doc['metadata']['title']
	# parts
	text_id = 0
	for part in ['abstract','body_text']:
		rec['part'] = part
		for x in doc[part]:
			text_id += 1
			rec['text_id'] = text_id
			#
			rec['text'] = x['text']
			rec['section'] = x['section']
			# bib
			rec['bib_titles'] = []
			for ref in x['cite_spans']:
				ref_id = ref['ref_id']
				if not ref_id: continue 
				ref_title = doc['bib_entries'][ref_id]['title'] # ERROR
				rec['bib_titles'] += [ref_title]
			# ref (tables and figures)
			rec['tables'] = []
			rec['figures'] = []
			for ref in x['ref_spans']:
				ref_id = ref['ref_id']
				if not ref_id: continue
				r = doc['ref_entries'][ref_id] # ERROR
				if r['type']=='table':
					rec['tables'] += [r['text']]
				if r['type']=='figure':
					rec['figures'] += [r['text']]
			yield rec

def all_records(limit=None):
	from itertools import islice
	for path in islice(list_data_files(),limit):
		yield from raw_to_records(path)

# ------------------------------------------------------------------------------

if __name__=="__main__":
	from pprint import pprint

			


	
