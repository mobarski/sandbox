from common import *

# REFERENCES:
## https://www.quantamagazine.org/new-ai-strategy-mimics-how-brains-learn-to-smell-20180918/
## http://science.sciencemag.org/content/sci/358/6364/793.full.pdf
## Memory Networks: https://arxiv.org/pdf/1410.3916.pdf

# TODO - FEATURES:
## test - learn X1 random vectors, check score before and after, check score for X2 random vectors before and after, plot how fast the error drops
## high perm -> slow targ change, low perm -> fast targ change
## score boosting based on high and/or low activity
## circular input (255 is close to 0)
## categorical input (hash8(x) -> eq=o_hi,ne=o_lo), dtype=uint16 ???
## input activity monitoring
## input average used in learning
## change permanence into its opposite (for target change) - avoid zeros
## int8 instead of uint8 ???
## moving averages
## e1 vs e2 in score calculation

# TODO - OPTIMIZE:
## convert dense-sparse in load/save
## sparsify targ - learn, load
## sparsify perm - learn, load
## score - multiprocessing
## score - numba
## score - numba+cuda

# ------------------------------------------------------------------------------

class onn:
	"""
	Olfaction based random Neural Network with inhibition (k-winners) and target values on synapses
	"""
	def __init__(self, n_in, n_out, n_conn, p_lo=1, p_hi=20, sparse=False):
		"""
		
		Parameters
		----------
			n_in -- number if inputs
			n_out -- number of outputs
			n_conn -- number of connections per output (:int) or ratio of connected inputs (:float)
			p_lo -- lowest initial permanence
			p_hi -- highest initial permanence
		"""
		self.dtype_perm = np.int8
		self.dtype_targ = np.uint8
		self.cfg = {}
		self.cfg['n_in'] = n_in
		self.cfg['n_out'] = n_out
		self.cfg['n_conn'] = int(n_conn*n_in) if type(n_conn) is float else n_conn
		self.cfg['p_lo'] = p_lo
		self.cfg['p_hi'] = p_hi
		self.cfg['sparse'] = sparse
		self.cnt = {}
		self.cnt['learn'] = 0
		self.cnt['score'] = 0
		self.conn = None # [i_out] -> set([i_in...])
		self.perm = None # [i_out][i_in] -> connection permanence
		self.targ = None 
		self.acti = None
		self.init()
	
	def init(self):
		"Initialize internal state (conn,perm,targ,acti)"
		cfg = self.cfg
		n_conn = cfg['n_conn']
		n_out = cfg['n_out']
		n_in = cfg['n_in']
		p_lo = cfg['p_lo']
		p_hi = cfg['p_hi']
		
		# connections
		conn = {}
		for i in range(n_out):
			conn[i] = combinations(n_in, n_conn)
		self.conn = conn
		
		if cfg['sparse']:
			# permanence
			perm = np.random.randint(p_lo,p_hi,(n_out,2,n_conn), self.dtype_perm)
			for i in conn:
				perm[i][0] = list(conn[i])
			self.perm = perm
			
			# targets
			targ = np.random.randint(0,255,(n_out,2,n_conn), self.dtype_targ)
			for i in conn:
				targ[i][0] = list(conn[i])
			self.targ = targ
		else:
			# permanence
			perm = np.zeros((n_out,n_in), self.dtype_perm)
			for i in conn:
				perm[i][list(conn[i])] = random_vector(p_lo, p_hi, n_conn)
			self.perm = perm
			
			# targets
			targ = np.zeros((n_out,n_in),self.dtype_targ)
			for i in conn:
				targ[i][list(conn[i])] = random_vector(0, 255, n_conn)
			self.targ = targ
		
		# activity
		self.acti = np.zeros(n_out,np.uint64)
	
	def save(self,f):
		"save network into file"
		version = 2
		p0 = f.tell()
		marshal.dump(self.cfg,  f, version)
		marshal.dump(self.conn, f, version)
		marshal.dump(self.cnt,  f, version)
		self.perm.tofile(f)
		self.targ.tofile(f)
		self.acti.tofile(f)
		return f.tell()-p0
	
	@staticmethod
	def load(f):
		"load network from file"
		self = onn(0,0,0)
		cfg = self.cfg = marshal.load(f)
		n_in = cfg['n_in']
		n_out = cfg['n_out']
		n_conn = cfg['n_conn']
		self.conn = marshal.load(f)
		self.cnt = marshal.load(f)
		if cfg['sparse']:
			pass # TODO
		else:
			self.perm = np.fromfile(f, self.dtype_perm, n_out*n_in).reshape(n_out, n_in)
			self.targ = np.fromfile(f, self.dtype_targ, n_out*n_in).reshape(n_out, n_in)
		self.acti = np.fromfile(f, np.uint64, n_out)
		return self
	
	# ---[ CORE ]---------------------------------------------------------------
	
	def score(self, input):
		"Calculate score for every output"
		conn = self.conn
		targ = self.targ
		n_conn = self.cfg['n_conn']
		score = {}
		for i in conn:
			selected = list(conn[i])
			vt = targ[i][selected].astype(np.int32)
			vi = input[selected]
			e1 = abs(vt-vi)
			e2 = e1**2
			accuracy = 255-e1
			score[i] = -1.0 * e2.sum()**0.5 / n_conn
		self.cnt['score'] += 1
		return score
	
	def learn(self, input, k, p_inc=10, p_dec=5, p_lo=1, p_hi=10, e_lo=10, e_hi=20):
		"""
		Parameters
		----------
			input -- input vector (:np.array)
			k -- number of winning neurons
			p_inc -- 
			p_dec -- 
			e_lo -- error threshold under which permanence will be increased (:int)
			e_hi -- error threshold above which permanance will be decreased (:int)
			p_lo -- lowest permanence for new connections (:int)
			p_hi -- highest permanence for new connections (:int)
		"""
		cfg = self.cfg
		conn = self.conn
		targ = self.targ
		perm = self.perm
		acti = self.acti
		n_in = cfg['n_in']
		n_conn = cfg['n_conn']
		# score
		score = self.score(input)
		# k winners take all
		winners = top(k, score)
		for w in winners:
			selected = list(conn[w])
			sel = np.array(selected)
			vt = targ[w][selected].astype(np.int)
			vi = input[selected]
			delta = vt-vi
			error = abs(delta)
			
			# update target
			targ[w][sel[delta >  99]] -= 50
			targ[w][sel[delta >   9]] -= 4
			targ[w][sel[delta >   2]] -= 1
			targ[w][sel[delta <  -2]] += 1
			targ[w][sel[delta <  -9]] += 4
			targ[w][sel[delta < -99]] += 50
			
			# update permanence
			perm[w][sel[error < e_lo]] += p_inc
			perm[w][sel[error > e_hi]] -= p_dec
			
			if 1:
				# remove connections
				old = perm[w][perm[w]<=0].nonzero()[0].tolist()
				perm[w][old] = 0
				conn[w].difference_update(old)
				
				# add new connections
				if old:
					new = set(combinations(n_in,len(old)))
					new.difference_update(conn[w])
					perm[w][list(new)] = random_vector(p_lo,p_hi,len(new))
					conn[w].update(new)
					targ[w][list(new)] = input[list(new)]
			
		# update activity
		acti[winners] += 1
		self.cnt['learn'] += 1
		
		return score

if __name__=="__main__":
	def fam(nn,x):
		s = sum(top(50,nn.score(x),values=True))
		return max(0,1000+s)/1000
	
	#NI = 40
	#NN = 1000
	#nn = onn(NI,NN,0.2,sparse=False)
	NI = 40
	NN = 8000
	t0=time()
	nn = onn(NI,NN,5,sparse=False)
	clock('init',t0)
	t0=time()
	s=nn.save(open('data/v2.onn','wb'))
	print(s/1000)
	clock('save',t0)
	x = random_sparse_vector(0,255,NI,0.3)
	print(top(10,nn.score(x),items=True))
	print(sum(top(50,nn.score(x),values=True)))
	print(fam(nn,x))
	for _ in range(20):
		nn.learn(x,50)
	print(sum(top(50,nn.score(x),values=True)))
	print(fam(nn,x))
	nn.save(open('data/v2.onn','wb'))
	nn2=nn.load(open('data/v2.onn','rb'))
	exit()
	print(fam(nn2,x))
