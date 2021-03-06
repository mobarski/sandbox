from common import *

# REFERENCES:
## https://www.quantamagazine.org/new-ai-strategy-mimics-how-brains-learn-to-smell-20180918/
## http://science.sciencemag.org/content/sci/358/6364/793.full.pdf


# TODO - FEATURES:
## negative connections - jak nie bedzie w in to trafia do neg, jak znowu nie bedzie to wypada
## medium connections - sygnal silny gdy wartosci blisko srodka

# TODO - OPTIMIZE:
## score - multiprocessing
## score - numba
## score - numba+cuda

class onn:
	"""
	Olfaction based random Neural Network with inhibition and binary weights
	"""
	def __init__(self, n_in, n_out, density=1.0, p_lo=10, p_hi=100):
		self.cfg = {}
		self.cfg['n_in'] = n_in
		self.cfg['n_out'] = n_out
		self.cfg['n_conn'] = int(density*n_in)
		self.cfg['p_lo'] = p_lo
		self.cfg['p_hi'] = p_hi
		self.cfg['density'] = density # remove ???
		self.conn = None # [i_out] -> set([i_in...])
		self.perm = None # [i_out][i_in] -> connection permanence
		self.init()
	
	def init(self):
		cfg = self.cfg
		n_conn = cfg['n_conn']
		n_out = cfg['n_out']
		n_in = cfg['n_in']
		p_lo = cfg['p_lo']
		p_hi = cfg['p_hi']
		
		# conn
		conn = {}
		for i in range(n_out):
			conn[i] = combinations(n_in, n_conn)
		self.conn = conn
		
		# perm
		if 0:
			perm = {}
			for i in conn:
				perm[i] = {j:p for j,p in zip(conn[i],random_vector(p_lo, p_hi, n_conn))}
			self.perm = perm
		else:
			perm = np.zeros((n_out,n_in),np.uint8)
			for i in conn:
				perm[i][list(conn[i])] = random_vector(p_lo, p_hi, n_conn)
			self.perm = perm
	
	def save(self,f):
		version = 2
		p0 = f.tell()
		marshal.dump(self.cfg,  f, version)
		marshal.dump(self.conn, f, version)
		if 0:
			marshal.dump(self.perm, f, version)
		else:
			self.perm.tofile(f)
		return f.tell()-p0
	
	@staticmethod
	def load(f):
		pass # TODO
	
	# ---[ CORE ]---------------------------------------------------------------
	
	def score(self, input):
		conn = self.conn
		score = {}
		for i in conn:
			score[i] = input[list(conn[i])].sum()
		return score
	
	def learn(self, input, k, p_inc=10, p_dec=5, p_min=20, p_lo=21, p_hi=40):
		cfg = self.cfg
		conn = self.conn
		perm = self.perm
		n_in = cfg['n_in']
		n_conn = cfg['n_conn']
		# score
		score = self.score(input)
		# k winners take all
		winners = top(k, score)
		for w in winners:
			# update perm
			avg = 1.0*score[w]/n_conn
			for i in conn[w]:
				perm[w][i] += p_inc if input[i] else -p_dec
				# TODO TEST only x best inputs improves perm
				# TODO TEST only x random inputs improves perm
				# TODO TEST only inputs above average improves perm, x random below average degrades perm
			# remove conn
			old = perm[w][perm[w]<p_min].nonzero()[0].tolist()
			perm[w][old] = 0
			conn[w].difference_update(old)
			# add new conn
			if old:
				new = set(combinations(n_in,len(old)))
				new.difference_update(conn[w])
				perm[w][list(new)] = random_vector(p_lo,p_hi,len(new))
				conn[w].update(new)

if __name__=="__main__":
	def fam(nn,x):
		s = sum(top(50,nn.score(x),values=True))
		return max(0,1000+s)/1000
	NI = 40
	NN = 1000
	nn = onn(NI,NN,0.2)
	x = random_sparse_vector(0,255,NI,0.3)
	print(top(10,nn.score(x),items=True))
	print(sum(top(50,nn.score(x),values=True)))
	exit()
	print(fam(nn,x))
	for _ in range(20):
		nn.learn(x,50)
	print(sum(top(50,nn.score(x),values=True)))
	print(fam(nn,x))
	nn.save(open('data/v1.onn','wb'))
	nn2=nn.load(open('data/v1.onn','rb'))
	exit()
	print(fam(nn2,x))
