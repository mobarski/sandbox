from common2 import *

# NAME IDEA -> pooling/random/sparse/distributed hebbian/horde/crowd/fragment/sample memory

# FEATURES:
# + boost -- neurons with empty mem slots learn faster
# + noise -- 
# + dropout -- temporal disabling of neurons
# + decay -- remove from mem
# + negatives -- learning to avoid detecting some patterns
# + fatigue -- winner has lower score for some time
# ~ sklearn -- compatibile api
# - prune -- if input < mem shrink mem ? (problem with m > input len)
# - weights -- sample weights for imbalanced classes
# - popularity -- most popular neuron is cloned / killed

# NEXT VERSION:
# - attention
#   - https://towardsdatascience.com/the-fall-of-rnn-lstm-2d1594c74ce0
#   - https://towardsdatascience.com/memory-attention-sequences-37456d271992
#   - https://medium.com/breathe-publication/neural-networks-building-blocks-a5c47bcd7c8d
#   - https://distill.pub/2016/augmented-rnns/
#   - http://akosiorek.github.io/ml/2017/10/14/visual-attention.html
#   + IDEA:
#     append activated neurons indexes to queue available as input
#     queue ages at constant rate and drops oldest values
#   - IDEA:
#     each neuron has small memory of activation prior to winning
#     this memory is compared to ctx and intersection added to score
#     winner updated this memory
#     OPTION: several memories with diferent time frames

# NEXT VERSION:
# - layers -- rsm stacking

# NEXT VERSIONS:
# - numpy -- faster version
# - cython -- faster version
# - gpu -- faster version
# - distributed 

class rsm:
	def __init__(self,n,m,c=0,**kw):
		"""Random Sample Memory
			n -- number of neurons
			m -- max connections per neuron (memory)
		"""
		self.mem = {j:set() for j in range(n)}
		self.win = {j:0 for j in range(n)}
		self.tow = {j:-42000 for j in range(n)} # time of win
		self.t = 0
		self.ctx = deque(maxlen=c) # context queue
		# cfg
		cfg = {}
		cfg['n'] = n
		cfg['m'] = m
		cfg['c'] = c
		cfg['k'] = kw.get('k',1)
		cfg['method'] = kw.get('method',1)
		cfg['cutoff'] = kw.get('cutoff',0.5)
		cfg['decay'] = kw.get('decay',0.0)
		cfg['dropout'] = kw.get('dropout',0.0)
		cfg['fatigue'] = kw.get('fatigue',0)
		cfg['boost'] = kw.get('boost',True)
		cfg['noise'] = kw.get('noise',True)
		cfg['sequence'] = kw.get('sequence',False)
		cfg.update(kw)
		self.cfg = cfg
	
	# ---[ core ]---------------------------------------------------------------
	
	def new_ctx(self):
		self.ctx.clear()
	
	# TODO -- input length vs mem length
	# TODO -- args from cfg
	def scores(self, input, raw=False, boost=False, noise=False, fatigue=0, dropout=0.0, **ignore): # -> dict[i] -> scores
		"""
			input -- sparse binary features
			raw -- disable all postprocessing
			boost -- improve scores based on number of unconnected synapses (TODO)
			noise -- randomize scores to prevent snowballing
			dropout -- temporal disabling of neurons
		"""
		mem = self.mem
		tow = self.tow
		N = self.cfg['n']
		M = self.cfg['m']
		t = self.t
		
		scores = {}
		for j in mem:
			scores[j] = len(set(input) & mem[j])
			
		if raw:
			return scores
			
		if noise:
			for j in mem:
				scores[j] += 0.9*random()
		if boost:
			for j in mem:
				scores[j] += 1+2*(M-len(mem[j])) if len(mem[j])<M else 0
			# TODO boost also based on low win ratio / low tow
		if fatigue:
			for j in mem:
				dt = 1.0*min(fatigue,t - tow[j])
				factor = dt / fatigue
				scores[j] *= factor
		if dropout:
			k = int(round(float(dropout)*N))
			for j in combinations(N,k):
				scores[j] = -1
		return scores
	
	
	def learn(self, input, negative=False, **ignore):
		for i in range(0,len(input),10):
			self.learn_(set(input[i:i+10]),negative=negative)
	
	def learn_(self, input, negative=False, **ignore):
		"""
			input -- sparse binary features
			k -- number of winning neurons
		"""
		mem = self.mem
		win = self.win
		tow = self.tow
		ctx = self.ctx
		t = self.t
		cfg = self.cfg
		M = self.cfg['m']
		N = self.cfg['n']
		k = self.cfg['k']
		decay = self.cfg['decay']
		sequence = self.cfg['sequence']
		
		known_inputs = set()
		for j in mem:
			known_inputs.update(mem[j])
		
		# context
		input = input | set(ctx)
		
		# scoring
		scores = self.scores(input, **cfg)
		winners = top(k,scores)
		
		for j in winners:
			
			# negative learning
			if negative:
				mem[j].difference_update(input)
				continue
			
			# positive learning
			unknown_inputs = input - known_inputs
			mem[j].update(pick(unknown_inputs, M-len(mem[j])))
			known_inputs.update(mem[j])

			# handle decay
			if decay:
				decay_candidates = mem[j] - input
				if decay_candidates:
					for d in decay_candidates:
						if random() < decay:
							mem[j].remove(d)
			
			# handle popularity
			win[j] += 1
			
			# handle fatigue
			tow[j] = t 
			
		# handle context
		if sequence:
			for i in range(len(ctx)):
				ctx[i] -= N
		for j in winners:
			ctx.append(-j-1)
			
		self.t += 1


	# ---[ auxiliary ]----------------------------------------------------------

	def fit(self, X, Y):
		cfg = self.cfg
		for x,y in zip(X,Y):
			negative = not y
			self.learn(x,negative=negative,**cfg)

	def fit2(self, X1, X0):
		cfg = self.cfg
		# TODO - unbalanced
		for x1,x0 in zip(X1,X0):
			self.learn(x1,negative=False,**cfg)
			self.learn(x0,negative=True,**cfg)
		

	def transform(self, X):
		cutoff = self.cfg['cutoff']
		out = []
		for s in self.score_many(X):
			y = 1 if s>=cutoff else 0
			out += [y]
		return out
	
	
	def fit_transform(self, X, Y):
		self.fit(X,Y)
		return self.transform(X)


	def score(self, X, Y, kind='acc'):
		c = self.confusion(X,Y)
		p = float(c['p'])
		n = float(c['n'])
		tp = float(c['tp'])
		tn = float(c['tn'])
		fp = float(c['fp'])
		fn = float(c['fn'])
		try:
			if kind=='acc':
				return (tp + tn) / (p + n)
			elif kind=='f1':
				return (2*tp) / (2*tp + fp + fn)
			elif kind=='prec':
				return tp / (tp + fp)
			elif kind=='sens':
				return tp / (tp + fn)
			elif kind=='spec':
				return tn / (tn + fp)
		except ZeroDivisionError:
			return float('nan')

	def confusion(self, X, Y):
		PY = self.transform(X)
		p = 0
		n = 0
		tp = 0
		tn = 0
		fp = 0
		fn = 0
		for y,py in zip(Y,PY):
			if y:  p+=1
			else:  n+=1
			
			if y:
				if py: tp+=1
				else:  fn+=1
			else:
				if py: fp+=1
				else:  tn+=1
		return dict(p=p,n=n,tp=tp,tn=tn,fp=fp,fn=fn)



	def score_many(self, X):
		out = []
		for x in X:
			s = self.score_one(x)
			out += [s]
		return out

	# TODO
	def calibrate(self, X, Y, kind='f1'):
		for i in range(1,20):
			c = 0.05*i
			self.set_params(cutoff=c)
			s = self.score(X,Y,kind)
			print'{} {:.3} -> {:.3}'.format(kind,c,s)
		

	def score_one(self, input):
		"aggregate scores to scalar"
		k = self.cfg['k']
		method = self.cfg['method']
		scores = self.scores(input)
		M = self.cfg['m']
		if method==0:
			return top(k, scores, values=True)
		elif method==1:
			score = 1.0*sum(top(k, scores, values=True))/(k*(M+1))
			return score
		elif method==2:
			score = 1.0*sum(top(k, scores, values=True))/(k*M)
			return min(1.0,score)
		if method==3:
			score = 1.0*min(top(k, scores, values=True))/(M+1)
			return score
		elif method==4:
			score = 1.0*min(top(k, scores, values=True))/M
			return min(1.0,score)
		if method==5:
			score = 1.0*max(top(k, scores, values=True))/(M+1)
			return score
		elif method==6:
			score = 1.0*max(top(k, scores, values=True))/M
			return min(1.0,score)


	def stats(self,prefix=''):
		N = self.cfg['n']
		M = self.cfg['m']
		mem_v = self.mem.values()
		out = {}
		# mem
		out['mem_empty']     = sum([1.0 if len(x)==0 else 0.0 for x in mem_v])/N
		out['mem_not_empty'] = sum([1.0 if len(x)>0 else 0.0 for x in mem_v])/N
		out['mem_full']      = sum([1.0 if len(x)==M else 0.0 for x in mem_v])/N
		out['mem_avg']       = sum([1.0*len(x) for x in mem_v])/(N*M)
		# win
		win = list(sorted(self.win.values()))
		out['win_min'] = win[0]
		out['win_max'] = win[-1]
		gini = 0
		for a in win:
			for b in win:
				gini += abs(a-b)
		gini = float(gini)/(2.0*len(win)*sum(win))
		out['win_gini'] = round(gini,3)
		# ctx
		out['ctx_mem_sum'] = sum([1 if x<0 else 0 for m in mem_v for x in m])
		out['ctx_mem_cnt'] = sum([max([1 if x<0 else 0 for x in m]) for m in mem_v if m])
		out['ctx_mem_max'] = max([sum([1 if x<0 else 0 for x in m]) for m in mem_v if m])
		#
		return {k:v for k,v in out.items() if k.startswith(prefix)}

	def set_params(self,**kw):
		self.cfg.update(kw)
	
	# TODO: deep parameter
	def get_params(self,deep=True):
		return self.cfg # TODO copy ???
