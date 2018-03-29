from collections import Counter,defaultdict

def get_stats(X,Y,base='df',stats='',agg='sum',norm='sum'):
	model = {}
	_stats = set(stats.split(' ')+[base,base+'_y'])
	_y = set(Y)
	
	for s in _stats:
		if s.endswith('_y'):
			model[s] = defaultdict(Counter)
		else:
			model[s] = Counter()
	
	# ==[ base ]============================================================
	
	for tokens,y in zip(X,Y):
		if 'tf' in _stats:
			tf = Counter(tokens)
			model['tf_y'][y].update(tf)
			model['tf'].update(tf)
		
		if 'df' in _stats:
			df = Counter(set(tokens))
			model['df_y'][y].update(df)
			model['df'].update(df)

	pass # TODO drop terms below treshold


	# ==[ stats ]===========================================================
	
	if 'chi_y' in _stats:
		pass # TODO
	
	if 'cmfs_y' in _stats:
		cnt_y = {}
		for y in _y:
			cnt_y[y] = Y.count(y) # TODO base=tf
		for t,f in model[base].items():
			for y in _y:
				f_y = model[base+'_y'][y].get(t,0)
				p_tc = 1.0 * f_y / cnt_y[y]
				p_ct = 1.0 * f_y / f
				model['cmfs_y'][y][t] = p_tc * p_ct
	
	if 'dia_y' in _stats:
		for t,f in model[base].items():
			for y in _y:
				f_y = model[base+'_y'][y].get(t,0)
				model['dia_y'][y][t] = 1.0 * f_y / f

	if 'gini_y' in _stats:
		cnt_y = {}
		for y in _y:
			cnt_y[y] = Y.count(y) # TODO base=tf
		for t,f in model[base].items():
			for y in _y:
				f_y = model[base+'_y'][y].get(t,0)
				p_tc = 1.0 * f_y / cnt_y[y]
				p_ct = 1.0 * f_y / f
				model['gini_y'][y][t] = p_tc*p_tc * p_ct*p_ct
	
	if 'wcp_y' in _stats:
		pass # TODO
	
	
	# TODO - my functions 
	
	# TODO *x_y - ballanced variants


	# ==[ aggregates ]======================================================
		
	if 'cmfs' in _stats:
		for t in model[base]:
			scores = [model['cmfs_y'][y][t] for y in _y]
			model['cmfs'][t] = max(scores) # TODO agg

	if 'dia' in _stats:
		for t in model[base]:
			scores = [model['dia_y'][y][t] for y in _y]
			model['dia'][t] = max(scores) # agg=sum always==1

	if 'gini' in _stats:
		for t in model[base]:
			scores = [model['gini_y'][y][t] for y in _y]
			model['gini'][t] = sum(scores) # always sum

	
	return model

if __name__=="__main__":
	X = ['ala ma kota','to jest test work ma','go go power ala ma','go work work kota ma']
	X = [x.split(' ') for x in X]
	Y = [0,1,1,0]
	m = get_stats(X,Y,'tf','gini_y gini')
	#print(m['dia_y'][0])
	#print(m['dia'])
	print(m['gini'])
