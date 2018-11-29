from common import *

# REFERENCES:
## https://www.quantamagazine.org/new-ai-strategy-mimics-how-brains-learn-to-smell-20180918/
## http://science.sciencemag.org/content/sci/358/6364/793.full.pdf


# TODO - FEATURES:
## negative connections - jak nie bedzie w in to trafia do neg, jak znowu nie bedzie to wypada
## avg connections - sygnal silny gdy mala odleglosc od sredniej

# TODO - OPTIMIZE:
## score - multiprocessing
## score - numba
## score - numba+cuda

# ------------------------------------------------------------------------------

class onn:
	"""
	Olfaction based Sparse/Random Neural Network with target values on neurons and k-winners
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
		self.targ = None 
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
		perm = np.zeros((n_out,n_in),np.uint8)
		for i in conn:
			perm[i][list(conn[i])] = random_vector(p_lo, p_hi, n_conn)
		self.perm = perm
		
		# targ
		self.targ = random_vector(0, 255, n_out)
	
	def save(self,f):
		version = 2
		p0 = f.tell()
		marshal.dump(self.cfg,  f, version)
		marshal.dump(self.conn, f, version)
		self.perm.tofile(f)
		self.targ.tofile(f)
		return f.tell()-p0
	
	@staticmethod
	def load(f):
		pass # TODO
	
	# ---[ CORE ]---------------------------------------------------------------
	
	def score(self, input):
		conn = self.conn
		targ = self.targ
		n_conn = self.cfg['n_conn']
		score = {}
		for i in conn:
			value = input[list(conn[i])].sum()
			avg = int(1.0*value/n_conn)
			score[i] = 255-abs(targ[i]-avg)
		return score
	
	# TODO
	def learn(self, input, k, p_inc=10, p_dec=5, p_min=20, p_lo=21, p_hi=40):
		cfg = self.cfg
		conn = self.conn
		targ = self.targ
		perm = self.perm
		n_in = cfg['n_in']
		n_conn = cfg['n_conn']
		# score
		score = self.score(input)
		# k winners take all
		winners = top(k, score)
		vt = targ[winners].astype(np.int16)
		vs = np.array([score[w] for w in winners])
		delta = vt-vi
		error = abs(delta)
		exit()
		for w in winners:
			selected = list(conn[w])
			for i in selected
	
			# TODO update term
			
			# TODO update perm
			#perm[w][sel[error <= avg_error]] += p_inc
			#perm[w][sel[error >  avg_error]] -= p_dec
			
			# # TODO remove conn
			# old = perm[w][perm[w]<p_min].nonzero()[0].tolist()
			# perm[w][old] = 0
			# conn[w].difference_update(old)
			
			# # TODO add new conn
			# if old:
				# new = set(combinations(n_in,len(old)))
				# new.difference_update(conn[w])
				# perm[w][list(new)] = random_vector(p_lo,p_hi,len(new))
				# conn[w].update(new)

if __name__=="__main__":
	NI = 10
	NN = 500
	nn = onn(NI,NN,0.5)
	x = random_vector(0,255,NI)
	print(sum(top(50,nn.score(x),values=True)))
	for _ in range(100):
		nn.learn(x,50)
	print(sum(top(50,nn.score(x),values=True)))
	
	
