from common2 import *

class rsm:
	def __init__(self,n,**kw):
		self.mem = {j:set() for j in range(n)}
		self.neg = {j:set() for j in range(n)}
		self.win = {}
		self.win[0] = {j:0 for j in range(n)}
		self.win[1] = {j:0 for j in range(n)}
		self.cfg = {'n':n}
		self.cfg.update(kw)
		self.defaults()
	
	def defaults(self):
		def default(k,v):
			self.cfg[k] = self.cfg.get(k,v)
		default('m',5)
		default('v',5)
		default('k',1)
		default('k0',self.cfg['k'])
		default('dropout',0.0)
		default('boost',1)
		default('noise',1)

	# ---[ core ]---------------------------------------------------------------
	
	def scores(self,input,learning=False):
		"return scores for all neurons"
		input = set(input)
		scores = {}
		mem = self.mem
		
		for j in mem:
			scores[j] = len(mem[j] & input)
		
		if learning:
			M = self.cfg['m']
			boost = self.cfg['boost']
			noise = self.cfg['noise']
			dropout = self.cfg['dropout']
		
			if boost:
				for j in mem:
					# TODO boost=2 -> need at least 2 items to not allocate new
					free = M-len(mem[j])
					used = len(mem[j])
					scores[j] += M+1 if used==0 else 0
			
			if noise:
				for j in mem:
					scores[j] += 0.9*random()
			
			if dropout:
				k = int(round(float(dropout)*N))
				for j in combinations(N,k):
					scores[j] = -1
		
		return scores
	
	# TODO attention -> sliding window
	
	def learn(self,input,y=1):
		input = set(input)
		mem = self.mem
		neg = self.neg
		M = self.cfg['m']
		V = self.cfg['v']
		K = self.cfg['k']
		K0 = self.cfg['k0']
		
		# negative
		if not y:
			scores = self.scores(input, learning=False)
			winners = top(K0,scores)
			for j in winners:
			
				common = input & mem[j]
				unknown = input - neg[j] - mem[j]
				mem[j].difference_update(common)
				old_neg = neg[j] - common
				# TODO mix old_neg and unknown
				new_neg = list(common) + list(old_neg) + list(unknown)
				#print('negative',common,old_neg,unknown)
				neg[j] = set(new_neg[:V])
		
		# positive
		else:
			scores = self.scores(input, learning=True)
			winners = top(K,scores)
			for j in winners:
					
				common = input & mem[j]
				old_mem = mem[j] - common
				unknown = input - mem[j] - neg[j]
				# TODO mix old_mem and unknown
				new_mem = list(common) + list(old_mem) + list(unknown)
				mem[j] = set(new_mem[:M])
		
		# count winners
		for j in winners:
			self.win[y][j] += 1
	
	# ---[ aux ]----------------------------------------------------------------
	
	def fit2(self, X1, X0):
		# TODO unbalanced
		for x1,x0 in zip(X1,X0):
			self.learn(x1,1)
			self.learn(x0,0)
	
	def transform(self, X):
		return list(self._transform(X))
	def _transform(self, X):
		for x in X:
			yield self.transform_one(x)
	
	# TODO attention -> sliding window
	def transform_one(self, x):
		M = self.cfg['m']
		scores = self.scores(x)
		k = 2 # TODO
		score = 1.0*sum(top(k,scores,values=True))/(M*k)
		return score

	def score(self, X, Y, kind='acc'):
		PY = self.transform(X)
		c = self.confusion(Y,PY,cutoff=0.1) # TODO cutoff
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

	def confusion(self, Y, PY, cutoff):
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
				if py>=cutoff: tp+=1
				else:  fn+=1
			else:
				if py>=cutoff: fp+=1
				else:  tn+=1
		return dict(p=p,n=n,tp=tp,tn=tn,fp=fp,fn=fn)

	def set_params(self,**kw):
		self.cfg.update(kw)

if __name__=="__main__":
	nn = rsm(5,m=5,v=5,k=2,boost=0)
	nn.learn([1,3,4,5],y=1)
	nn.learn([1,5,7,9],y=0)
	nn.learn([1,3,4,9],y=1)
	print(nn.mem)
	print(nn.neg)
	print(nn.win)
	print(nn.transform_one([1,3,4,5,7,9]))
