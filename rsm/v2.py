from common2 import *

# NAME IDEA -> pooling/random/sparse/distributed hebbian/horde/crowd/fragment/sample memory
# NAME IDEA -> Fruit Fly Memory

class rsm:
	def __init__(self,n,m,v):
		"""Random Sample Memory
			n -- number of neurons
			m -- max hard connections per neuron
			v -- max soft connections per neuron
		"""
		self.N = n
		self.M = m
		self.V = v
		self.mem = {j:set() for j in range(n)}
		self.vol = {j:set() for j in range(n)}
	
	
	def score(self, input, boost=True): # -> dict[i] -> score
		"""
			input -- sparse binary features
			boost -- improve score based on number of unconnected synapses (TODO)
		"""
		mem = self.mem
		vol = self.vol
		M = self.M
		V = self.V
		score = {}
		for j in mem:
			score[j] = len(input & mem[j]) + 1.0*len(input & vol[j])/(V+1)
		if boost:
			for j in mem:
				score[j] += 1+M if len(mem[j])<M else 0
		return score
	
	
	def learn(self, input, k):
		"""
			input -- sparse binary features
			k -- number of winning neurons
		"""
		mem = self.mem
		vol = self.vol
		#
		score = self.score(input)
		winners = top(k,score)
		for j in winners:
			
			# handle confirmed -> add to mem, remove from vol
			free_mem = self.M - len(mem[j])
			confirmed = vol[j] & input
			# memorized
			mem_delta = self.pick(confirmed, free_mem)
			mem[j].update(mem_delta)
			vol[j].difference_update(mem_delta)
			# TODO - mem decay
			
			# handle unknown -> add to vol
			known = mem[j] & input
			unknown = input - known - confirmed
			not_comfirmed = vol[j] - confirmed
			not_memorized = confirmed - set(mem_delta) # must stay in vol
			new_vol = []
			new_vol += list(not_memorized)
			new_vol += list(unknown) # TODO: proportion of mix 
			new_vol += list(not_comfirmed) # TODO: proportion of mix 
			free_vol = self.V - len(vol[j])
			vol[j] = set(new_vol[:self.V])
			
	
	@classmethod
	def pick(self,v_set,n):
		"select n random values from a set"
		# TODO random
		out = list(v_set)
		shuffle(out)
		return out[:n]
	
	@classmethod
	def sparsify(self, input):
		"Transform dense binary vector into sparse binary features"
		return set([i for i,v in enumerate(input) if v]) # indexes of active inputs


	def stats(self):
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
		return out


if __name__ == "__main__":
	X = [random_vector(100,0,1) for i in range(100)]
	X = list(map(rsm.sparsify,X))
	nn = rsm(50,7,13)
	s=nn.score(X[0])
	print(sum(s.values()))
	for i in range(2):
		for x in X:
			nn.learn(x,1)
	s=nn.score(X[0])
	print(sum(s.values()))
	from pprint import pprint
	pprint(nn.stats())
	pprint(nn.mem)
	pprint(nn.vol)
