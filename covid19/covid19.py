import inverness
model = inverness.Model('model_1000/').load()

task = "Outcomes data for COVID-19 after mechanical ventilation adjusted for age"

# TODO sprawdzanie zakresu -1,+2

results = model.tfidf_query('mouse|mice|^rats|sheep|^pig$|pigs|piglet|cavia|rabbit')
for ti,token,df in zip(*results):
	print(ti,token,df)
#exit()

q = "mechanical ventilation"
for method,fun in [('dense',model.find_dense),('sparse',model.find_sparse)]:
	print(f'\n{method.upper()}:')
	top = fun(q,5)
	for i,d,m in top:
		doc = model.get_doc(i)
		text = model.doc_to_text(doc).replace('\n',' ').replace('\r',' ')
		doc2 = model.get_doc(i+1)
		text2 = model.doc_to_text(doc2).replace('\n',' ').replace('\r',' ')		
		print(f"{d:.03f}  {i}  {text} {text2}")
	print()



# TODO do modelu -> TAK TAK TAK !!!
def multi_query(*args):
	ids = set()
	for i,arg in enumerate(args):
		query,_,exclude = arg.partition(' ~~ ')
		q_ids = model.inverted_query(query,exclude)
		if i==0:
			ids.update(q_ids)
		else:
			ids.intersection_update(q_ids)
	return ids

print('\nINVERTED:')
#ids1 = model.inverted_query('^mecha')
ids1 = model.inverted_query('^female|^male')
ids2 = model.inverted_query('^ventilated')
print(f"len1:{len(ids1)}  len2:{len(ids2)}  len1&2:{len(ids1&ids2)}")
for i in ids1&ids2:
	doc = model.get_doc(i)
	text = model.doc_to_text(doc).replace('\n',' ').replace('\r',' ')
	print(f"{i}  {text}")

print(len(multi_query('^mecha','^ventilated')))

# 'mecha','ventil'

from gensim.matutils import cossim
def sim(a,b):
	return cossim(enumerate(a),enumerate(b))
a1 = model.text_to_dense('mouse')
a2 = model.text_to_dense('sheep')
a3 = model.text_to_dense('mice')
x1 = model.text_to_dense('mechanical')
x2 = model.text_to_dense('ventilation')
x3 = model.text_to_dense('female')

x12 = model.text_to_dense('mechanical ventilation')
exit()
