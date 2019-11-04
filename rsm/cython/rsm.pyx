
# TODO gdy k=1 to winners mozna zapamietac w scores (ale dropout) -> przesunac dropout do scores
# TODO atencja tutaj czy poziom wyzej?
# TODO dropout tutaj czy poziom wyzej?
# TODO sortowanie wynikow
# TODO refaktoryzacja score do funkcji?
def scores(int [:,:] mem, int [:] input, int [:] out):
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


def learn_positive(int [:,:] mem, int [:,:] neg, int [:] input, int [:] out):
	cdef int activated
	cdef int i,j
	cdef k = 3
	# remove neg from input ??? or later @ update ???
	
	
	# add context to input
	pass
	
	# scores
	activated = scores(mem, input, out)
	if activated==0:
		pass # TODO -- boosting
	
	# dropout -- czy w scores ??? raczej tam
	pass
	
	# noise -- low priority ??? moze tez w scores ???
	pass
	
	# select winners
	winners = np.argsort(out)
	
	# update winners
	for i in range(k):
		j = winners[i]
		# select input to add
		# - omit neg
		# - mem & input - must be kept        --> te dwa zawsze sie zmieszcza !!!
		# - rest of mem mem - should be kept  --> te dwa zawsze sie zmieszcza !!!
		# - rest of input - nice to keep
	
	# update context
	pass

def learn_negative():
	pass # TODO

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
