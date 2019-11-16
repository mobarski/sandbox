from common2 import *

# NAME IDEA -> pooling/random/sparse/distributed hebbian/horde/crowd/fragment/sample memory

# FEATURES:
# + boost (TODO vol?)
# + noise
# + dropout -- temporal disabling of neurons
# + decay -- move from mem to vol
# + negatives -- learning to avoid detecting some patterns
# - prune -- if input < mem perform fast decay
# - fatigue -- winner has lower score for some time

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
	def __init__(self,n,m,v):
		"""Random Sample Memory
			n -- number of neurons
			m -- max hard connections per neuron (memory)
			v -- max soft connections per neuron (volatile memory)
		"""
		self.N = n
		self.M = m
		self.V = v
		self.mem = {j:set() for j in range(n)}
		self.vol = {j:set() for j in range(n)}
		self.win = set() # NEW fatigue
	
	
	def scores(self, input, boost=False, noise=False, dropout=0.0): # -> dict[i] -> scores
		"""
			input -- sparse binary features
			boost -- improve scores based on number of unconnected synapses (TODO)
			noise -- randomize scores to prevent snowballing
			dropout -- temporal disabling of neurons
		"""
		mem = self.mem
		vol = self.vol
		N = self.N
		M = self.M
		V = self.V
		scores = {}
		for j in mem:
			scores[j] = len(input & mem[j])
			scores[j] += 1.0*len(input & vol[j])/(V+1)
		if noise:
			for j in mem:
				scores[j] += 1.0/(V+2)*random()
		if boost:
			for j in mem:
				scores[j] += 1+2*(M-len(mem[j])) if len(mem[j])<M else 0
		if dropout:
			k = int(round(float(dropout)*N))
			for j in combinations(N,k):
				scores[j] = -1
		return scores
	
	
	def learn(self, input, k, decay=0.0, dropout=0.0, quick=False, negative=False):
		"""
			input -- sparse binary features
			k -- number of winning neurons
		"""
		mem = self.mem
		vol = self.vol
		M = self.M
		V = self.V
		
		# quick learning
		if quick and not negative:
			known_inputs = set()
			for j in mem:
				known_inputs.update(mem[j])
				known_inputs.update(vol[j])
		
		
		scores = self.scores(input, boost=True, noise=True, dropout=dropout)
		winners = top(k,scores)
		for j in winners:
			
			# negative learning
			if negative:
				vol[j].difference_update(input)
				mem[j].difference_update(input)
				continue
			
			# quick learning
			if quick:
				if len(mem[j])==0:
					unknown_inputs = input - known_inputs
					mem[j].update(self.pick(unknown_inputs, M))
					known_inputs.update(mem[j])
			
			confirmed = vol[j] & input # must be done before decay

			# handle decay
			if decay and random()<decay:
				decay_candidates = mem[j] - input
				if decay_candidates:
					d_list = list(decay_candidates)
					shuffle(d_list)
					d = d_list[0]
					mem[j].remove(d)
					if V:
						vol[j].add(d)

			# handle confirmed
			# -> add to mem, remove from vol
			free_mem = self.M - len(mem[j])
			mem_delta = self.pick(confirmed, free_mem)
			mem[j].update(mem_delta)
			vol[j].difference_update(mem_delta)
			
			# handle unknown
			# -> add to vol
			known = mem[j] & input
			unknown = input - known - confirmed
			not_comfirmed = vol[j] - confirmed
			not_memorized = confirmed - set(mem_delta) # must stay in vol
			new_vol = list(unknown) + list(not_comfirmed) # TODO: proportion
			shuffle(new_vol)
			new_vol = list(not_memorized) + new_vol
			vol[j] = set(new_vol[:V])

		#print(scores) # XXX
		
		# TODO handle fatigue

	
	@classmethod
	def pick(self,v_set,n):
		"select n random values from a set"
		# TODO random
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
		out['v_empty']     = sum([1.0 if len(x)==0 else 0.0 for x in vol_v])/self.N
		out['v_not_empty'] = sum([1.0 if len(x)>0 else 0.0 for x in vol_v])/self.N
		out['v_full']      = sum([1.0 if len(x)==self.V else 0.0 for x in vol_v])/self.N
		out['m_avg']       = sum([1.0*len(x) for x in mem_v])/(self.N*self.M)
		out['v_avg']       = sum([1.0*len(x) for x in vol_v])/(self.N*self.V)
		return {k:v for k,v in out.items() if k.startswith(prefix)}

