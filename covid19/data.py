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

# ---[ sentences ]--------------------------------------------------------------

# TODO - refactor do model_data.py ???

from text import text_to_sentences, text_to_tokens

def rec_to_sentences(rec):
	for field in ['section','text']:
		sentences = text_to_sentences(rec[field])
		yield from sentences
	for field in ['tables','figures','bib_titles']:
		for text in rec[field]:
			sentences = text_to_sentences(text)
			yield from sentences			

def rec_to_tokens(rec):
	tokens = []
	sentences = rec_to_sentences(rec)
	for text in sentences:
		tokens.extend(text_to_tokens(text))
	return tokens

def all_records_as_tokens(limit=None):
	for rec in all_records(limit):
		yield rec_to_tokens(rec)

def all_sentences_as_text(limit=None):
	for rec in all_records(limit):
		yield from rec_to_sentences(rec)

def all_sentences_as_tokens(limit=None):
	for text_sen in all_sentences_as_text(limit):
		yield text_to_tokens(text_sen)

# ------------------------------------------------------------------------------

if __name__=="__main__":
	from pprint import pprint
	if 0:
		path = 'data/biorxiv_medrxiv/biorxiv_medrxiv/00d16927588fb04d4be0e6b269fc02f0d3c2aa7b.json'
		#path = 'data/custom_license/custom_license/0a3a221e70ed8497ac197567fe69e7d384759826.json'
		for rec in convert_one(path):
			pprint(rec)
	if 0:
		path = list(list_data_files())[0]
		print(path)
		for rec in raw_to_records(path):
			#pprint(rec)
			pprint(list(rec_to_sentences(rec)))
	if 0:
		for x in all_sentences_as_text(2):
			print(x)
	if 1:
		for x in all_sentences_as_tokens(2):
			print(x)
			


	
