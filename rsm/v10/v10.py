from common2 import *

# TODO - prog aktywacji >= n wejsc
# TODO - boost sprawdzic i poprawic

# TODO - boost na podstawie win[0] win[1]
# TODO - prog aktywacji >= n slow (nie poprzednich stanow)
# TODO - ctx rosnie tylko gdy dobre dopasowanie

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
		self.ctx = deque(maxlen=self.cfg['c']) # context queue
		# NEW
		self.cnt = {j:Counter() for j in range(n)}
	
	def defaults(self):
		def default(k,v):
			self.cfg[k] = self.cfg.get(k,v)
		default('m',5)
		default('v',5)
		default('k',1)
		default('c',0)
		default('k0',self.cfg['k'])
		default('dropout',0.0)
		default('boost',1)
		default('noise',0.9)
		default('sequence',False)
		default('awidth',10)
		default('astep',5)
		default('cutoff',0.1)
		default('penalty',3)

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
			N = self.cfg['n']
			boost = self.cfg['boost']
			noise = self.cfg['noise']
			dropout = self.cfg['dropout']
		
			if boost:
				max_s = max(scores.values())
				if max_s <= boost: # NEW
					for j in mem:
						s = scores[j]
						free = M-len(mem[j])
						used = len(mem[j])
						scores[j] += M+1 if used==0 else 0 # TODO variants
			
			if noise:
				for j in mem:
					scores[j] += noise*random()
			
			if dropout:
				k = int(round(float(dropout)*N))
				for j in combinations(N,k):
					scores[j] = -1
		
		return scores
	

	def learn(self,input,y=1):
		self.ctx.clear()
		a_w = self.cfg['awidth']
		a_o = self.cfg['astep']
		for i in range(0,len(input),a_o):
			self.learn_part(input[i:i+a_w],y)

	
	def learn_part(self,input,y=1):
		input = set(input)
		mem = self.mem
		neg = self.neg
		ctx = self.ctx
		M = self.cfg['m']
		C = self.cfg['c']
		V = self.cfg['v']
		K = self.cfg['k']
		K0 = self.cfg['k0']
		sequence = self.cfg['sequence']
		
		# context
		input = input | set(ctx)
		
		# negative
		if not y:
			penalty = self.cfg['penalty']
			scores = self.scores(input, learning=False)
			winners = top(K0,scores,items=True)
			for j,s in winners:
				if not s: continue
				common = input & mem[j]
				unknown = input - neg[j] - mem[j]
				if penalty==0:
					mem[j].difference_update(common)
				else:
					self.cnt[j].subtract({x:penalty for x in common}) # TODO config
					removed = [x for x,cnt in self.cnt[j].items() if cnt<1]
					mem[j].difference_update(removed)
					common = set(removed)
					if 0:
						for x in removed:
							del self.cnt[j][x]
				old_neg = neg[j] - common
				new_neg = list(common) + list(old_neg)
				new_neg = [x for x in new_neg if x>=0] # !!!
				#print('negative',common,old_neg,unknown)
				new_neg = set(new_neg[:V]) 
				neg[j] = new_neg
				# counters
				if 1:
					cnt = Counter({x:self.cnt[j][x] for x in mem[j]})
					self.cnt[j] = cnt
		
		# positive
		else:
			scores = self.scores(input, learning=True)
			winners = top(K,scores,items=True)
			for j,s in winners:

				# TODO mix old_mem and unknown
				vacant = M - len(mem[j])				
				if vacant:
					unknown = input - mem[j] - neg[j]
					unknown = list(unknown)
					if unknown:
						shuffle(unknown)
						mem[j].update(unknown[:vacant])
				# counter
				if 1:
					cnt = Counter({x:self.cnt[j][x] for x in mem[j]})
					cnt.update(mem[j] & input)
					self.cnt[j] = cnt
		

		# handle context
		if C:
			N = self.cfg['n']
			if sequence:
				for i in range(len(ctx)):
					ctx[i] -= N
			for j,s in winners:
				if s==0 and y==0: continue
				ctx.append(-j-1)

		
		# count winners
		for j,s in winners:
			if s==0 and y==0: continue
			self.win[y][j] += 1
	
	# ---[ aux ]----------------------------------------------------------------
	
	def fit2(self, X1, X0):
		# TODO unbalanced
		shuffle(X1)
		shuffle(X0)
		for x1,x0 in zip(X1,cycle(X0)):
			self.learn(x1,1)
			self.learn(x0,0)			

	
	def transform(self, X):
		return list(self._transform(X))
	def _transform(self, X):
		for x in X:
			yield self.transform_one_v3(x)
	
	# attention -> sliding window
	def transform_one_v3(self, x):
		self.ctx.clear()
		M = self.cfg['m']
		a_w = self.cfg['awidth']
		a_o = self.cfg['astep']
		#
		all_scores = []
		for i in range(0,len(x),a_o):
			scores = self.scores(x[i:i+a_w])
			all_scores += [scores]
		# agg scores and all_scores
		scores_agg = []
		for scores in all_scores:
			#score = 1.0*sum(top(1,scores,values=True))/M
			score = 1.0*max(scores.values())/M # if k==1
			scores_agg += [score]
		score = sum(scores_agg)/len(scores_agg)
		return score

	# NO ATTENTION VERSION
	def transform_one_v1(self, x):
		self.ctx.clear()
		M = self.cfg['m']
		scores = self.scores(x)
		k = 6 # TODO
		score = 1.0*sum(top(k,scores,values=True))/(M*k)
		return score

	# NO ATTENTION VERSION
	def transform_one_v2(self, x):
		self.ctx.clear()
		M = self.cfg['m']
		scores = self.scores(x)
		k = 3 # TODO
		score = 1.0*sum([x if x>=2 else 0 for x in top(k,scores,values=True)])/(M*k)
		return score

	# TODO cutoff jako cfg
	def score(self, X, Y, kind='acc'):
		cutoff = self.cfg['cutoff']
		PY = self.transform(X)
		c = self.confusion(Y,PY,cutoff=cutoff)
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

	def calibrate(self, X, Y, kind='f1'):
		for i in range(1,20):
			c = 0.002*i
			self.set_params(cutoff=c)
			s = self.score(X,Y,kind)
			print'{} {:.3} -> {:.3}'.format(kind,c,s)

	def calibrate2(self, X1, Y1, X2, Y2, kind='f1'):
		for i in range(1,20):
			c = 0.002*i
			self.set_params(cutoff=c)
			s1 = self.score(X1,Y1,kind)
			s2 = self.score(X2,Y2,kind)
			print'{} {:.3} ->\t{:.3}\t{:.3}'.format(kind,c,s1,s2)


	def set_params(self,**kw):
		self.cfg.update(kw)

if __name__=="__main__":
	nn = rsm(5,m=5,v=5,k=2,boost=1)
	nn.learn([1,3,4,5],y=1)
	nn.learn([1,5,7,9],y=0)
	nn.learn([1,3,4,9],y=1)
	print(nn.mem)
	print(nn.neg)
	print(nn.win)
	print(nn.transform_one([1,3,4,5,7,9]))
