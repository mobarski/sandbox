from common2 import *

# NAME IDEA -> pooling/random/sparse/distributed hebbian/horde/crowd/fragment/sample memory

# FEATURES:
# + boost -- neurons with empty mem slots learn faster
# + noise -- 
# + dropout -- temporal disabling of neurons
# + decay -- remove from mem
# + negatives -- learning to avoid detecting some patterns
# + fatigue -- winner has lower score for some time
# - prune -- if input < mem shrink mem ? (problem with m > input len)

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
			mem[j].update(self.pick(unknown_inputs, M-len(mem[j])))
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

	
	@classmethod
	def pick(self,v_set,n):
		"select n random values from a set"
		if n<=0: return []
		out = list(v_set)
		shuffle(out)
		return out[:n]


	# auxiliary

	def score(self, input, k=1, method=1):
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

