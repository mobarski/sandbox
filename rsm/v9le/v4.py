from common2 import *

# NAME IDEA -> pooling/random/sparse/distributed hebbian/horde/crowd/fragment/sample memory

# FEATURES:
# + boost -- neurons with empty mem slots learn faster
# + noise -- 
# + dropout -- temporal disabling of neurons
# + decay -- remove from mem
# + negatives -- learning to avoid detecting some patterns
# + fatigue -- winner has lower score for some time
# - sklearn -- compatibile api
# - prune -- if input < mem shrink mem ? (problem with m > input len

# IDEA:
# - popularity -- most popular neuron is cloned / killed

# NEXT VERSION:
# - layers -- rsm stacking

# NEXT VERSION:
# - attention
#   - https://towardsdatascience.com/the-fall-of-rnn-lstm-2d1594c74ce0
#   - https://towardsdatascience.com/memory-attention-sequences-37456d271992


# NEXT VERSION:
# - numpy -- faster version
# - cython -- faster version
# - gpu -- faster version
# - distributed 

class rsm:
	def __init__(self,n,m):
		"""Random Sample Memory
			n -- number of neurons
			m -- max connections per neuron (memory)
		"""
		self.N = n
		self.M = m
		self.mem = {j:set() for j in range(n)}
		self.win = {j:0 for j in range(n)}
		self.tow = {j:-42000 for j in range(n)} # time of win
		self.t = 0
	
	# ---[ core ]---------------------------------------------------------------
	
	# TODO -- input length vs mem length
	def scores(self, input, boost=False, noise=False, fatigue=0, dropout=0.0): # -> dict[i] -> scores
		"""
			input -- sparse binary features
			boost -- improve scores based on number of unconnected synapses (TODO)
			noise -- randomize scores to prevent snowballing
			dropout -- temporal disabling of neurons
		"""
		mem = self.mem
		tow = self.tow
		N = self.N
		M = self.M
		t = self.t
		scores = {}
		for j in mem:
			scores[j] = len(input & mem[j])
		if noise:
			for j in mem:
				scores[j] += 0.9*random()
		if boost:
			for j in mem:
				scores[j] += 1+2*(M-len(mem[j])) if len(mem[j])<M else 0
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
	
	
	def learn(self, input, k, decay=0.0, dropout=0.0, fatigue=0,
	          negative=False, boost=True, noise=True):
		"""
			input -- sparse binary features
			k -- number of winning neurons
		"""
		mem = self.mem
		win = self.win
		tow = self.tow
		M = self.M
		t = self.t
		
		known_inputs = set()
		for j in mem:
			known_inputs.update(mem[j])
		
		scores = self.scores(input, boost=boost, noise=noise, dropout=dropout, fatigue=fatigue)
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

		self.t += 1


	# ---[ auxiliary ]----------------------------------------------------------

	def fit(self, X, Y):
		for x,y in zip (X,Y):
			negative = not y
			self.learn(x,negative=negative)

	def score_many(self, X, k=1, method=1):
		out = []
		for x in X:
			s = self.score_one(x,k,method)
			out += [s]
		return out


	def transform(self, X, k=1, method=1, cutoff=0.5):
		out = []
		for s in self.score_many(X,k,method):
			y = 1 if s>=cutoff else 0
			out += [y]
		return out


	def confusion(self, X, Y, k=1, method=1, cutoff=0.5):
		PY = self.transform(X,k,method,cutoff)
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


	def score(self, X, Y, k=1, method=1, cutoff=0.5, kind='acc'):
		c = self.confusion(X,Y,k,method,cutoff)
		p = float(c['p'])
		n = float(c['n'])
		tp = float(c['tp'])
		tn = float(c['tn'])
		fp = float(c['fp'])
		fn = float(c['fn'])
		if kind=='f1':
			return (2*tp) / (2*tp + fp + fn)
		elif kind=='acc':
			return (tp+tn) / (p+n)
		elif kind=='prec':
			return tp / (tp + fp)
		elif kind=='sens':
			return tp / (tp + fn)
		elif kind=='spec':
			return tn / (tn + fp)


	def score_one(self, input, k=1, method=1):
		"aggregate scores to scalar"
		scores = self.scores(input)
		if method==0:
			return top(k, scores, values=True)
		elif method==1:
			score = 1.0*sum(top(k, scores, values=True))/(k*(self.M+1))
			return score
		elif method==2:
			score = 1.0*sum(top(k, scores, values=True))/(k*self.M)
			return min(1.0,score)
		if method==3:
			score = 1.0*min(top(k, scores, values=True))/(self.M+1)
			return score
		elif method==4:
			score = 1.0*min(top(k, scores, values=True))/self.M
			return min(1.0,score)
		if method==5:
			score = 1.0*max(top(k, scores, values=True))/(self.M+1)
			return score
		elif method==6:
			score = 1.0*max(top(k, scores, values=True))/self.M
			return min(1.0,score)


	def stats(self,prefix=''):
		vol_v = self.vol.values()
		mem_v = self.mem.values()
		out = {}
		out['m_empty']     = sum([1.0 if len(x)==0 else 0.0 for x in mem_v])/self.N
		out['m_not_empty'] = sum([1.0 if len(x)>0 else 0.0 for x in mem_v])/self.N
		out['m_full']      = sum([1.0 if len(x)==self.M else 0.0 for x in mem_v])/self.N
		out['m_avg']       = sum([1.0*len(x) for x in mem_v])/(self.N*self.M)
		return {k:v for k,v in out.items() if k.startswith(prefix)}

