import numpy as np

# random numbers - requires POSIX
cdef extern from "stdlib.h":
	double drand48()
	long int lrand48()
	void srand48(long int seedval)
cdef extern from "time.h":
	long int time(int)
srand48(time(0))

# TODO wyniki trzymane jako x[0]=len x[1:len]=data zamiast konczone 0
#      -> lepsza wydajnosc bo nie trzeba czyscic ???
# TODO atencja tutaj czy poziom wyzej?
#      -> poziom wyzej -> i tak kod jest trudny
# TODO refaktoryzacja score do funkcji?
# TODO czy hit faktycznie potrzebne?
#      - raczej tak -> podstawa do lagodnego rozpadu (decay)
#      - neg moze zmniejszac hit o 1,2 lub 3 i dopiero jak <=0 wypada ???


def scores(int [:,:] mem, int [:] input, int [:] out, int [:,:] hit, float dropout=0.0):
	cdef int N = mem.shape[0]
	cdef int M = mem.shape[1]
	cdef int I = input.shape[0]
	cdef int n = 1
	cdef int j,i,x
	cdef int i1=0 # index of first matching item
	cdef int score
	cdef int activated = 0
	
	for j in range(N):
		if dropout:
			if drand48() < dropout:
				print(j,'dropout') # XXX
				out[j]=-1
				continue
			
		score,x,i = 0,0,0
		while True:
			if i>=M:
				break
			elif x>=I:
				break
			elif mem[j,i]==0:
				break
			elif input[x]==0:
				break
			elif input[x]==mem[j,i]:
				score += 1
				i += 1
				x += 1
				# register hits
				if 1:
					if 0: # TODO ktore podejscie wybrac ???
						hit[j,i] += 1
					else:
						if score==1:
							i1 = i
						elif score==2:
							hit[j,i1] += 1
							hit[j,i] += 1
						else:
							hit[j,i] += 1
			elif input[x]<mem[j,i]:
				x += 1
			elif input[x]>mem[j,i]:
				i += 1
		out[j] = score
		if score>=2:
			activated += 1
	return activated


def learn_positive(int [:,:] mem, int [:,:] neg, int [:] input, int [:] out, int [:] used, int[:,:] hit, float dropout=0.0, int k=1):
	cdef int N = mem.shape[0]
	cdef int M = mem.shape[1]
	cdef int V = neg.shape[1]
	cdef int I = input.shape[0]
	cdef int activated
	cdef int i,j,xi,xm,xv,xc,C,xs,S,xt
	cdef new_cnt
	cdef int [:] candidates = np.zeros(M, dtype=np.int32)
	cdef int [:] shortlist  = np.zeros(M, dtype=np.int32)
	cdef int [:] tmp1 = np.zeros(M, dtype=np.int32)
	cdef int [:] tmp2 = np.zeros(M, dtype=np.int32)
	
	# add context to input
	pass
	
	# scores
	activated = scores(mem, input, out, hit, dropout)
	if activated==0:
		print('activated==0') # XXX
		pass # TODO -- boosting <--------------------------------------------- 3
	
	# select winners
	winners = np.argsort(out)[::-1] # descending order of scores
	print('winners',winners) # XXX
	
	# update winners
	for i in range(k):
		j = winners[i] # take highest score
		print # XXX
		print(j,'score',out[j]) # XXX
		# handle dropout -> omit neuron
		if out[j]<0:
			print(j,'dropout') # XXX
			continue
		
		# decay items with lowest hits
		pass
		
		# select candidates to add to mem (omit neg)
		if M-used[j] == 0: continue # no room in mem
		candidates[:] = 0
		xi,xm,xv = 0,0,0
		xc = 0
		while True:
			# print(j,'candidates loop',xi,xm,xv) # XXX
			if xi>=I: break
			elif input[xi]==0: break
			elif xv<V and input[xi]==neg[j,xv]:
				xi += 1
				xv += 1
			elif xv<V and neg[j,xv]<input[xi]:
				xv += 1
			elif xm>=M:
				candidates[xc] = input[xi]
				xc += 1
				xi += 1
			elif mem[j,xm]==input[xi]:
				xm += 1
				xi += 1
			elif mem[j,xm]<input[xi]:
				xm += 1
			elif mem[j,xm]>input[xi]:
				candidates[xc] = input[xi]
				xc += 1
				xi += 1
			else:
				print('X_X') # XXX
				return -1 # ERROR ???
		C = xc
		print(j,'candidates',C,list(candidates)) # XXX
		
		# shortlist candidates
		if C==0: continue
		shortlist[:] = 0
		S = M-used[j]
		if C<S: S=C
		
		# randomize
		shuffle_trim_sort(candidates, shortlist, tmp1, C, S)
		
		print(j,'shortlist',S,list(shortlist)) # XXX
		
		# add candidates from shortlist to mem and move hit counters
		tmp1[:] = 0
		tmp2[:] = 0
		xm,xs,xt = 0,0,0
		while True:
			#print(j,'update loop',xm,xs,xt) # XXX
			if xt>=M: break
			elif (xm>=M or mem[j,xm]==0) and (xs>=S or shortlist[xs]==0): break
			elif xm>=M or mem[j,xm]==0:
				tmp1[xt] = shortlist[xs]
				tmp2[xt] = 1
				xs += 1
				xt += 1
			elif xs>=S or shortlist[xs]==0:
				tmp1[xt] = mem[j,xm]
				tmp2[xt] = hit[j,xm]
				xm += 1
				xt += 1
			elif mem[j,xm] < shortlist[xs]:
				tmp1[xt] = mem[j,xm]
				tmp2[xt] = hit[j,xm]
				xm += 1
				xt += 1
			elif mem[j,xm] > shortlist[xs]:
				tmp1[xt] = shortlist[xs]
				tmp2[xt] = 1
				xs += 1
				xt += 1
			else:
				print('X_X') # XXX
				return -1

		mem[j,:] = tmp1[:]
		hit[j,:] = tmp2[:]
		#print(j,'after',list(mem[j,:])) # XXX
		
		# update used
		used[j] = xt

	# update context
	pass


def learn_negative(int [:,:] mem, int [:,:] neg, int [:] input, int [:] out, int [:] used, int[:,:] hit, float dropout=0.0, int k=1):
	# TODO ograniczyc do tego co faktycznie jest uzywane
	cdef int N = mem.shape[0]
	cdef int M = mem.shape[1]
	cdef int V = neg.shape[1]
	cdef int I = input.shape[0]
	cdef int activated
	cdef int i,j,xi,xm,xv,xc,C,xs,S,xt,U
	cdef new_cnt
	cdef int [:] candidates = np.zeros(V, dtype=np.int32)
	cdef int [:] shortlist  = np.zeros(V, dtype=np.int32)
	cdef int [:] tmp1 = np.zeros(M, dtype=np.int32)
	cdef int [:] tmp2 = np.zeros(M, dtype=np.int32)
	cdef int [:] tmp3 = np.zeros(V, dtype=np.int32)

	# add context to input
	pass
	
	# scores
	activated = scores(mem, input, out, hit, dropout)
	if activated==0:
		print('activated==0') # XXX

	# select winners
	winners = np.argsort(out)[::-1] # descending order of scores
	print('winners',winners) # XXX
	
	# update winners
	for i in range(k):
		j = winners[i] # take highest score
		print # XXX
		print(j,'score',out[j]) # XXX
		
		# handle dropout -> omit neuron
		if out[j]<0:
			print(j,'dropout') # XXX
			continue
			
		# handle no common words -> omit neuron ???
		if out[j]==0:
			print(j,'no common words') # XXX
			continue
		
				
		# neg decay -> wybieramy z not in input
		pass
		
		# candidates
		xc,xv,xi = 0,0,0
		candidates[:]=0
		while True:
			if xi>=I or input[xi]==0 or xc>=V: break
			elif xv>=V or neg[j,xv]==0:
				candidates[xc] = input[xi]
				xi += 1
				xc += 1
			elif neg[j,xv] == input[xi]:
				xv += 1
				xi += 1
			elif input[xi] < neg[j,xv]:
				candidates[xc] = input[xi]
				xc += 1
				xi += 1
			elif input[xi] > neg[j,xv]:
				xv += 1
			else:
				print('X_X') # ??? ERROR
				return -1
		U = xv
		C = xc
		print(j,'neg candidates',C,list(candidates),U) # XXX
			
		# shortlist
		S = V-U
		if C<S: S=C
		shuffle_trim_sort(candidates, shortlist, tmp1, C, S)
		print(j,'shortlist',S,list(shortlist)) # XXX
		
		
		# TODO update 
		xs,xv,xt = 0,0,0
		tmp3[:] = 0
		while True:
			print(j,'neg loop',xv,xi,xt) # XXX
			if xt>=V: break
			elif (xs>=S or shortlist[xs]==0) and (xv>=V or neg[j,xv]==0): break
			elif xs>=S or shortlist[xs]==0:
				tmp3[xt] = neg[j,xv]
				xt += 1
				xv += 1
			elif xv>=V or neg[j,xv]==0:
				tmp3[xt] = shortlist[xs]
				xt += 1
				xs += 1
			elif shortlist[xs] < neg[j,xv]:
				tmp3[xt] = shortlist[xs]
				xt += 1
				xs += 1
			elif shortlist[xs] > neg[j,xv]:
				tmp3[xt] = neg[j,xv]
				xt += 1
				xv += 1
			elif shortlist[xs] == neg[j,xv]:
				tmp3[xt] = neg[j,xv]
				xt += 1
				xv += 1
				xs += 1
		neg[j,:] = tmp3[:]
		print(j,'negative',list(neg[j,:])) # XXX
		
		
		# remove input from mem and remove hits
		xm,xi,xt = 0,0,0
		tmp1[:] = 0
		tmp2[:] = 0
		while True:
			print(j,'negative mem loop',xm,xi,xt) # XXX
			if xm>=M or mem[j,xm]==0: break
			elif xi>=I or input[xi]==0:
				tmp1[xt] = mem[j,xm]
				tmp2[xt] = hit[j,xm]
				xt += 1
				xm += 1
			elif input[xi]==mem[j,xm]:
				xi += 1
				xm += 1
			elif mem[j,xm]<input[xi]:
				tmp1[xt] = mem[j,xm]
				tmp2[xt] = hit[j,xm]
				xt += 1
				xm += 1
			elif mem[j,xm]>input[xi]:
				xi += 1
			else:
				print('X_X') # XXX
				return -1 # ERROR
		print(j,'tmp1',list(tmp1)) # XXX
		print(j,'tmp2',list(tmp2)) # XXX
		mem[j,:] = tmp1[:]
		hit[j,:] = tmp2[:]
		
		# update used cells
		used[j] = xt


cdef shuffle_trim_sort(int [:] data, int [:] out, int [:] tmp, int N, int K):
	"sorted combination from sorted data - works in linear time"
	cdef int i,j,x
	out[:] = 0
	
	# just rewrite
	if N==K:
		out[:N] = data[:N]
		return
	
	# prepare indexes
	for i in range(N):
		tmp[i] = i
		
	# shuffle indexes using https://en.wikipedia.org/wiki/Fisher-Yates_shuffle
	for i in range(N-1):
		j = i + lrand48()%(N-i)
		tmp[j],tmp[i] = tmp[i],tmp[j] # swap
	print('tmp after shuffle',list(tmp)) # XXX
	
	# sparse output
	for i in range(K):
		x = tmp[i]
		out[x] = data[x]
	print('output before compact',list(out)) # XXX
	
	# compact output
	cdef int O = out.shape[0]
	j = 0
	for i in range(O):
		if out[i]:
			out[j] = out[i]
			if i!=j:
				out[i] = 0
			j += 1
	print('output after compact',list(out)) # XXX
		

# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

# TODO array.array vs np.array performance and code readability

def test1(int [:,:] mem, int [:] input):
	cdef int N = mem.shape[0]
	cdef int M = mem.shape[1]
	cdef int n = 1
	cdef int j,x
	
	for j in range(N):
		for x in range(M):
			mem[j,x] = n
			n += 1


# wersja zakladajaca posortowany input i mem 
def test2(int [:,:] mem, int [:] input, int [:] out):
	cdef int N = mem.shape[0]
	cdef int M = mem.shape[1]
	cdef int I = input.shape[0]
	cdef int n = 1
	cdef int j,i,x
	cdef int score
	cdef int activated = 0

	for j in range(N):
		score,x,i = 0,0,0
		while True:
			if i>=M:
				break
			elif x>=I:
				break
			elif mem[j,i]==0:
				break
			elif input[x]==0:
				break
			elif input[x]==mem[j,i]:
				score += 1
				i += 1
				x += 1
			elif input[x]<mem[j,i]:
				x += 1
			elif input[x]>mem[j,i]:
				i += 1
		out[j] = score
		if score>=2:
			activated += 1
	return activated


# NIE UZYWAMY - sporo wolniejsze
# wersja zakladajaca nieposortowany mem i input
def test3(int [:,:] mem, int [:] input, int [:] out):
	cdef int N = mem.shape[0]
	cdef int M = mem.shape[1]
	cdef int I = input.shape[0]
	cdef int n = 1
	cdef int j,i,x
	cdef int score

	for j in range(N):
		score = 0
		for i in range(M):
			for x in range(I):
				if input[x]==0: break
				if input[x]==mem[j,i]:
					score += 1
			if mem[j,i]==0: break	
		out[j] = score
