from common import *

# TODO rename -> pooling/random/sparse/distributed hebbian/horde/crowd/fragment/sample memory
# NEW NAME: random sample memory / fruit fly memory

# TODO vol/mem_cnt_score_boost
# TODO focus
# TODO focus boost
# TODO noise boost
# TODO auto noise
# TODO auto focus

class rsm:
	def __init__(self, n, m):
		self.mem = {j:set() for j in range(n)} # memory
		self.vol = {j:set() for j in range(n)} # volatile memory -- "Once is never. Twice is always."
		self.free = {j:m for j in range(n)}
		self.mem_cnt = {}
		self.vol_cnt = {}
		self.ofreq = {j:0 for j in range(n)} # output frequency
		self.noise = set() # ignored inputs
		self.focus = set() # valuable inputs
		self.cfg = dict(n=n,m=m)
		self.cnt = 0
	
	def save(self, f):
		v=2
		pos0 = f.tell()
		marshal.dump(self.cfg,f,v)
		marshal.dump(self.mem,f,v)
		marshal.dump(self.vol,f,v)
		marshal.dump(self.mem_cnt,f,v)
		marshal.dump(self.vol_cnt,f,v)
		marshal.dump(self.free,f,v)
		marshal.dump(self.ofreq,f,v)
		marshal.dump(self.noise,f,v)
		marshal.dump(self.focus,f,v)
		marshal.dump(self.cnt,f,v)
		return f.tell()-pos0
	
	def score(self, input, boost=False):
		""
		inp = set(input) - self.noise
		mem = self.mem
		free = self.free
		free_score_boost = 0.9
		if boost:
			score = {j:free_score_boost*free[j]+len(inp & mem[j]) for j in mem}
		else:
			score = {j:len(inp & mem[j]) for j in mem}
		return score
	
	def learn(self, input, k):
		mem = self.mem
		vol = self.vol
		mem_cnt = self.mem_cnt
		vol_cnt = self.vol_cnt
		free = self.free
		ofreq = self.ofreq
		
		self.cnt += 1
		
		inp = set(input) - self.noise
		score = self.score(input, boost=True)
		winners = top(k,score)
		for j in winners:
			ofreq[j] += 1 # update output frequency
			
			# known inputs
			known = inp & mem[j]
			confirmed = inp & vol[j] # confirmed: seen for the second time
			vol[j].difference_update(confirmed)
			for i in confirmed:
				vol_cnt[i] -= 1
			
			# unknown inputs
			unknown = inp - mem[j]
			u_by_f = list(unknown) # TODO
			if free[j]:
				# TODO .focus
				new = u_by_f[:free[j]]
				if new:
					mem[j].update(new)
					vol[j].update(new)
					free[j] -= len(new)
					for i in new:
						mem_cnt[i] = mem_cnt.get(i,0)+1
						vol_cnt[i] = vol_cnt.get(i,0)+1
			elif unknown:
				# TODO how many ???
				if vol[j]:
					# TODO random pick using mem_cnt and vol_cnt
					# TODO .focus
					i = vol[j].pop()
					mem[j].remove(i)
					mem_cnt[i] -= 1
					vol_cnt[i] -= 1
				elif confirmed:
					# TODO random pick using mem_cnt and vol_cnt
					# TODO .focus
					i = confirmed.pop()
					mem[j].remove(i)
					mem_cnt[i] -= 1
				else:
					# TODO random pick using mem_cnt and vol_cnt
					# TODO .focus
					i = mem[j].pop()
					mem_cnt[i] -= 1
				i = u_by_f[0] # TODO .focus
				mem[j].add(i)
				vol[j].add(i)
				mem_cnt[i] = mem_cnt.get(i,0)+1
				vol_cnt[i] = vol_cnt.get(i,0)+1
				
		return score
	
	# not used
	def forget(self,value):
		"remove value from memory"
		mem = self.mem
		free = self.free
		for j in mem:
			if value in mem[j]:
				mem[j].remove(value)
				free[j] += 1


if __name__=="__main__":
	t0=time()
	mm = rsm(100,5)
	clock('init',t0)
	X = [random_vector(0,9,40) for _ in range(10)]
	x = X[0]
	t0 = time()
	s = mm.score(x)
	clock('score',t0)
	print(sum(top(3,s,values=True)))
	t0 = time()
	for _ in range(10):
		for x in X:
			mm.learn(x,10)
	clock('learn',t0)
	for x in X:
		s = mm.score(x)
		print(sum(top(3,s,values=True)))
	t0=time()
	size=mm.save(open('data/v1.model','wb'))
	clock('save',t0)
	print('size:',size//1024,'KB')
	