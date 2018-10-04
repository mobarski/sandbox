
################################################################################

# IDEA konfiguracja -> dim/msr:nazwa:fun:i1,i2
# TODO dim w pamieci vs redis

################################################################################

def split(data,dim,dim_i=[],keep_i=[]):
	done = []
	todo = []
	missing = {i:set() for i in dim_i}
	for rec in data:
		if not rec: continue
		m_cnt = 0
		for i in dim_i:
			if rec[i] not in dim[i]:
				missing[i].add(rec[i])
				m_cnt += 1
		if m_cnt:
			todo.append(rec)
			continue
		out = []
		for i in dim_i:
			out.append(dim[i][rec[i]])
		for i in keep_i:
			out.append(rec[i])
		done.append(out)
			
	missing = {i:missing[i] for i in missing if missing[i]}
	return done,todo,missing

def add_missing_single(d,m):
	id = len(d)+1
	for v in m:
		d[v] = id
		id += 1

def add_missing(dim,missing):
	for i in missing:
		add_missing_single(dim[i],missing[i])

################################################################################

if __name__=="__main__":
	from pprint import pprint

	data = [
		[]
		,[11,'aa','bb','cc',3,8.15]
		,[12,'aa','xx','zz',4,3.35]
		,[13,'xx','bb','cc',7,2.95]
		,[14,'aa','dd','cc',3,1.85]
	]

	data2 = [
		[]
		,[23,'xx','xx','xx',1,1.11]
		,[24,'aa','dd','zz',2,2.22]
	]

	dim = {i:{} for i in [1,2,3]}

	done,todo,missing = split(data,dim,[1,2,3],[0,4,5])
	add_missing(dim,missing)
	done,todo,missing = split(todo,dim,[1,2,3],[0,4,5])

	pprint(done)
	#print(todo)
	#print(missing)

	done,todo,missing = split(data2,dim,[1,2,3],[0,4,5])
	print(done)
	add_missing(dim,missing)
	done,todo,missing = split(todo,dim,[1,2,3],[0,4,5])
	pprint(done)
	#print(todo)
	#print(missing)
