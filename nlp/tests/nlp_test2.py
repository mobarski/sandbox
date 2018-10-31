import sys; sys.path.append('..')

from nlp import *

if __name__ == "__main__":
	from time import time
	import pandas as pd
	import numpy as np
	import pickle
	import marshal
	
	def my_preproc(text):
		return text.lower()
	
	test_re = re.compile(r'\ba\w{4,6}\b',re.U)
	def my_tokenizer(text):
		return test_re.findall(text)
	
	t0=time()
	lem_dict = marshal.load(open('../data/lem_dict.mrl','rb'))
	print('lem_dict',int(time()-t0),'s')
	def my_postproc(tokens):
		out = []
		for t in tokens:
			lem = lem_dict.get(t)
			if not lem: continue
			out.append(lem)
		return out
	def my_postproc2(tokens):
		out = []
		for t in tokens:
			lem = lem_dict.get(t)
			if not lem: continue
			out.append(t)
		return out
	
	if 1:
		frame = pd.read_csv('../data/__all__.txt',sep='\t',header=None,names=['col','id','text'])
		t0=time()
		#df = get_df(frame.text,12,min_df=10,max_df=0.5)
		#dfy = get_dfy(frame.text,frame.col,workers=12,min_df=10,analyzer='char',ngram_range=(3,4))
		if 0:
			dfy = get_dfy(frame.text,frame.col,workers=12,min_df=10,postprocessor=my_postproc2)
			pickle.dump(dfy,open('../data/nlp_dfy.pickle','wb'))
			col = frame.col
			pickle.dump(col,open('../data/nlp_col.pickle','wb'))
		else:
			dfy = pickle.load(open('../data/nlp_dfy.pickle','rb'))
			col = pickle.load(open('../data/nlp_col.pickle','rb'))
		for y in dfy:
			print(y,len(dfy[y]))
		print('dfy',time()-t0,'s')
		
		t0=time()
		topic = 'automaniak'
		
		if 0:
			df = get_df_from_dfy(dfy)
			chi = get_chi(df,len(frame.text),dfy[topic],Counter(frame.col)[topic])
			top_chi_words = [t for t,v in chi.most_common(100)]
			dfy = get_dfy(frame.text,frame.col,workers=12,min_df=10,ngram_range=(2,2),ngram_words=top_chi_words,stop_words=['a','i','o','w','z','u','na','do','lub'])
		
		df = get_df_from_dfy(dfy)
		for topic in [topic]:
			chi = get_chi(df,len(frame.text),dfy[topic],Counter(frame.col)[topic])
			chi_ex = get_chi_explain(df,len(frame.text),dfy[topic],Counter(frame.col)[topic])
			for t,v in chi.most_common(100):
				print(topic,t,v,df[t],dfy[topic][t])#,chi_ex[t])
		
		print('chi',time()-t0)
		print(len(df))
		
		t0=time()
		vocabulary = [t for t,v in chi.most_common(100)]
		vectorized = vectorize(frame.text, vocabulary=vocabulary,
			workers=12, postprocessor=my_postproc2,
			sparse=True, binary=True,
			dtype=None)
		print('vectorize',time()-t0)
		print(len(marshal.dumps(vectorized)))
		marshal.dump(vectorized,open('../data/nlp_vectorized.marshal','wb'))
		marshal.dump(vocabulary,open('../data/nlp_vocabulary.marshal','wb'))
	else:
		t0=time()
		vectorized = marshal.load(open('../data/nlp_vectorized.marshal','rb'))
		vocabulary = marshal.load(open('../data/nlp_vocabulary.marshal','rb'))
		print('vectorize',time()-t0,'s')
	
	vectorized = chain.from_iterable(vectorized)
	t0 = time()
	coy = get_coy(vectorized,col,diagonal=False,binary=True,
		triangular=True,
		upper_limit=0,output_dtype=np.uint16,output_len=100)
	co = get_co_from_coy(coy,dtype=np.uint16)
	#print(co)
	print('co',time()-t0,'s')
	if 0:
		for (t1,t2),f in co.most_common(100):
			print(t1,t2,f,vocabulary[t1],vocabulary[t2])
	print('co.pickle',len(pickle.dumps(co)))
	#print('co.marshal',len(marshal.dumps(dict(co))))
	print('co.marshal',len(marshal.dumps(co)))
	# print(min(df.values()))
	# for t,v in df.most_common(10):
		# print(t,v)
	
	# t0=time()
	# idf = get_idf(df,n,min_df=10)
	# for t,v in idf.most_common(10):
		# print(t,v,df[t])
	# print(time()-t0)
