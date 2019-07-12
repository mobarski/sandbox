# encoding: utf8
from __future__ import print_function
import sqlite3
from time import time
from collections import Counter,defaultdict
from itertools import groupby
import re

from pprint import pprint # XXX

# ver: 2019-07-05T15

class Token(unicode):
	def __init__(self,text):
		self.text = text

def _analyze(tokens, dict_db):
	"""
	Dla każdego tokenu zwraca rekordy z morfeusza
	"""
	# TODO opcja do filtrowania pos itp
	aux = {'t':[]}
	aux['t'] += [time()]
	db = dict_db
	aux['t'] += [time()]
	db.execute('attach ":memory:" as mem')
	db.execute('create table mem.doc (i,word,word_lower)')
	db.executemany('insert into mem.doc values (?,?,?)',((i,word,word.lower()) for i,word in enumerate(tokens)))
	out = db.execute('select i,mem.doc.word,xxx.* from mem.doc left join xxx on xxx.word==mem.doc.word_lower and pos not in ("brev","depr")').fetchall()
	db.execute('detach mem')
	aux['t'] += [time()]
	return out,aux

def genders(gender_str):
	"""zamienia ciag okreslajacy plec w liste plci bez powtorzen"""
	#yield gender_str or ''
	if gender_str:
		if 'm' in gender_str: yield 'm'
		if 'f' in gender_str: yield 'f'
		if 'n' in gender_str: yield 'n'

def analyze(tokens, dict_db, mark=['lem','pos']):
	aux = {'t':[time()]}
	db = dict_db
	results,__aa = _analyze(tokens, db)
	aux['t'] += [time()]
	aux['analysis'] = results
	aux['analysis_aux'] = __aa
	# zbior konca zdan
	eos_set = set([-1])
	aux['eos']=eos_set
	lem_i_list = defaultdict(set)
	lem_gen = {}
	#results = list(map(list,results)) # NEW - do zmiany w miejscu
	# debug
	if 0:
		for r in results: print(r)
		print('REMEMBER TO TURN OFF THE DEBUG MODE !!!')
		exit()
	# filtrowanie
	if 1:
		_results = []
		for x in results:
			if x[9]=='nazwisko' and not x[1][0].isupper(): continue
			_results.append(x)
		results = _results
	# zliczanie lematow + bonus za zgodnosc lematu ze slowem
	# + zbieranie dopelniaczy
	if 1:
		eos_re = re.compile('[.?!]+')
		lem_cnt = Counter()
		ood = Counter() # out of dict
		for x in results:
			lem = x[3]
			if not lem and x[1][0].isupper():
				ood[x[1]] += 1
			lem_cnt[lem] += 1
			if lem==x[1].lower():
				lem_cnt[lem] += 5 # bonus
			if 'name' in mark:
				if not x[2] and eos_re.match(x[1]):
					eos_set.add(x[0])
			# dopelniacze
			if x[5]=='gen':
				lem_gen[lem] = x[2]
		ood_lem = get_prefix_map(ood)
		aux['ood'] = ood
		aux['ood_lem'] = ood_lem
		aux['lem_gen'] = lem_gen
		aux['t'] += [time()]
	# wybor najsilniejszego lematu
	out = []
	grouped = groupby(results,lambda x:x[0])
	grouped = [(g,list(rec)) for g,rec in grouped] # materialize iterators
	candidates = dict(grouped) # i -> list of candidate records
	#aux['candidates'] = candidates
	c_capital_first = Counter()
	c_capital_all = Counter()
	c_begin = Counter()
	c_lem = Counter()
	for g,rec in grouped:
		rec = list(rec)
		t = Token(rec[0][1])
		t.i = rec[0][0]
		t.eos = int(t.i in eos_set)
		# candidates
		if 'lem' in mark:
			t._lem = list(set([r[3] for r in rec]))
		if 'pos' in mark:
			t._pos = list(set([r[4] for r in rec]))
		if 'gender' in mark:
			t._gender = list(set([g for r in rec for g in genders(r[7])]))
		if 'case' in mark:
			t._case = list(set([r[5] for r in rec]))
			#t._case = list(set(['{}:{}:{}'.format(g,r[6],r[5]) for r in rec for g in genders(r[7])]))
		# selected
		if 'lem' in mark:
			c1 = Counter({r[3]:lem_cnt[r[3]] for r in rec})
			t.lem = c1.most_common(1)[0][0] or ood_lem.get(rec[0][1],rec[0][1]) # TODO config
			c_lem[t.lem] += 1
			lem_i_list[t.lem].add(r[0])
		if 'pos' in mark:
			c2 = Counter({r[4]:lem_cnt[r[3]] for r in rec})
			t.pos = c2.most_common(1)[0][0]
		if 'name' in mark:
			c3 = Counter({r[9]:lem_cnt[r[3]] for r in rec})
			t.name = c3.most_common(1)[0][0]
			capital_first = int(t[0].isupper())
			capital_all = int(t.isupper())
			begin = int(t.i-1 in eos_set)
			c_capital_first[t.lem] += capital_first
			c_capital_all[t.lem] += capital_all
			c_begin[t.lem] += begin
		if 'gender' in mark:
			c4 = Counter({g:lem_cnt[r[3]] for r in rec for g in genders(r[7])}) # TODO wiele plci w jednym rekordzie m1,m2,m3,f,n
			t.gender = c4.most_common(1)[0][0] if c4 else ''
		# TODO aux/debug
		out.append(t)
	if 'name' in mark:
		for t in out:
			t.all_caps = 1.0*c_capital_all[t.lem]/c_lem[t.lem]
			t.capital = 1.0*c_capital_first[t.lem]/c_lem[t.lem]
			t.begin = c_begin[t.lem]
			if t.capital<1.0: # nazwiska typu Piatek, Zgoda
				t.name=''
			if t.name=='nazwa_pospolita':
				t.name=''
			if t.capital==1.0 and c_capital_first[t.lem]>t.begin:
				t_lem = t.lem
				t.lem = t.lem.capitalize()
				lem_i_list[t.lem] = lem_i_list[t_lem]
				if not t.name:
					t.name='nazwa?'
			if t.all_caps==1.0:
				t_lem = t.lem
				t.lem = t.lem.upper()
				lem_i_list[t.lem] = lem_i_list[t_lem]
				if not t.name:
					t.name='nazwa?'
	aux['lem_i_list'] = lem_i_list
	# frazy
	if 'phrase' in mark:
		c_phr = Counter()
		t_dict = {}
		w_to_t = {t.lem:t for t in out}
		#w_to_t = {unicode(t):t for t in out}
		#w_to_t.update({unicode(t):t for t in out})
		phr_i_list = defaultdict(list)
		for a,b in zip(out,out[1:]):
			if a.eos or b.eos: continue
			if a.pos=='subst' or b.pos=='subst' or a.name or b.name:
				if 1:
					c_phr[a.lem,b.lem] += 1
					phr_i_list[a.lem,b.lem] += [a.i]
					t_dict[a.lem,b.lem] = (a,b)
				else: # experimental - do not use
					c_phr[a,b] += 1
					phr_i_list[a,b] += [a.i]
		bi = {k:v for k,v in c_phr.most_common() if v>1 or (k[0][0].isupper() and k[-1][0].isupper())}
		# ngramy: n > 2
		if 1:
			for a,b in bi:
				for i in phr_i_list[a,b]:
					if i>0 and not out[i-1].eos:
						pass
						# c_phr[out[i-1].lem,a,b] += 1
						# t_dict[out[i-1].lem,out[i].lem,out[i+1].lem] = out[i-1],out[i],out[i+1]
						# if i+2<len(out) and not out[i+2].eos:
							# c_phr[out[i-1].lem,a,b,out[i+2].lem] += 1
							# t_dict[out[i-1].lem,out[i].lem,out[i+1].lem,out[i+2].lem] = out[i-1],out[i],out[i+1],out[i+2]
					# TODO len(out) vs i
					if i+2<len(out) and not out[i+2].eos:
						# 3-gram
						c_phr[a,b,out[i+2]] += 1
						t_dict[out[i].lem,out[i+1].lem,out[i+2].lem] = out[i],out[i+1],out[i+2]
						# 4-gram OFF
						if not out[i+3].eos:
							c_phr[a,b,out[i+2].lem,out[i+3].lem] += 1
							t_dict[out[i].lem,out[i+1].lem,out[i+2].lem,out[i+3].lem] = out[i],out[i+1],out[i+2],out[i+3]
			phr = {k:v for k,v in c_phr.most_common() if v>1 or (k[0][0].isupper() and k[-1][0].isupper())}
		else:
			phr = bi
		common_end = set(['w','na','to','do','i','o','z','gdy',u'być',u'się','ten','bo','po','lub','dla','ma','ze','jest','no','za','a','u','od','mi','albo',u'że',u'mieć','oba','nie',u'mój','czy','on',u'już','wraz',u'mieć'])
		common_start = common_end - set(['nie','oba','bez',u'mój'])
		sep = set(['-',':','(',')','[',']','"'])
		# separatory nie sa dozwolone
		phr = {k:v for k,v in phr.items() if len(set(k)&sep)==0}
		# slowa pospolite nie sa dozwolone na poczatku i koncu
		phr = {k:v for k,v in phr.items() if k[0] not in common_start and k[-1] not in common_end}
		# usuwamy bezokoliczniki - na razie nie zamieniamy ich w nic sensownego
		phr = {k:v for k,v in phr.items() if not sum([int(w.endswith(u'ić') or w.endswith(u'ać') or w.endswith(u'ść') or w.endswith(u'eć') or w.endswith(u'być')) for w in k])}
		# EXPERIMENTAL - uzgadnianie rodzaju, na razie tylko dla bi
		if 1:
			_phr = {}
			for k in phr:
				if 0:
					# na razie uzgadnianie rodzaju dziala tylko dla bigramow
					if len(k)>2:
						_phr[k] = phr[k]
						continue
					w1,w2 = k
					t1,t2 = t_dict[k]
					# TODO refactor
					if t1.pos=='adj' and t2.pos=='subst':
						w1 = set_adj_gender(w1,t2.gender)
					elif t1.pos=='subst' and t2.pos=='adj':
						w2 = set_adj_gender(w2,t1.gender)
					# EXPERIMENTAL - dopelniacz
					elif t1.pos=='subst' and t2.pos=='subst':
						#w2 = w2+u'***'
						pass
					_phr[w1,w2] = phr[k]
				else:
					w = list(k)
					inf_cnt = 0
					for i,_ in enumerate(w):
						t = w_to_t.get(w[i])
						if not t: continue
						if 0:
							# wykrywanie bezokolicznikow
							if t.pos=='fin' and w[i].endswith(u'ć'):
								inf_cnt += 1
						# uzgadnianie rodzaju przymiotnikow
						if t.pos=='subst':
							before = range(i-1,-1,-1)
							after = range(i+1,len(w))
							for loop_range in [before,after]:
								for j in loop_range:
									t2 = w_to_t.get(w[j])
									if not t2: continue
									if t2.pos=='adj':
										w_j = w[j]
										w[j] = set_adj_gender(w[j], t.gender)
										if w[j] != w_j:
											lem_i_list[w[j]] = lem_i_list[w_j]
									else:
										break
							# NEW uzgadnianie statystyczne (liczba, przypadek)
							j = i+1
							if 1 and j<len(w):
								t2 = w_to_t.get(w[j])
								if t2 and t2.pos=='subst':
									w_j = w[j]
									#w[j] = lem_gen.get(t2.lem,w[j])
									a = lem_i_list[t.lem]
									b = lem_i_list[t2.lem]
									bigram_i_list = get_bigram_i_list(a,b)
									a_adj_cnt = 0
									b_cnt = Counter()
									for bi in bigram_i_list:
										for c in candidates[bi]:
											if c[4]=='adj':
												a_adj_cnt += 1
										for c in candidates[bi+1]:
											b_cnt[c[2]] += 1
									if a_adj_cnt==0:
										w[j] = b_cnt.most_common(1)[0][0]
									if w[j] != w_j:
										if w_j[0].isupper():
											if w_j[-1].isupper():
												w[j] = w[j].upper()
											else:
												w[j] = w[j].capitalize()
										#w[j]+=u'***' # oznaczenie do latwego debugowania
										lem_i_list[w[j]] = lem_i_list[w_j]
					w_new = tuple(w)
					if inf_cnt==0:
						_phr[w_new] = phr[k]
			phr = _phr
		aux['phr'] = phr
	aux['t'] += [time()]
	return out,aux

# ------------------------------------------------------------------------------

def get_prefix_map(words,min_len=2):
	"""zwraca slownik mapujacy wartosc na prefix bedacy inna wartoscia"""
	out = {}
	for _,words in groupby(sorted(words),lambda x:x[0]):
		words = list(sorted(words,key=lambda x:len(x)))
		for i in range(len(words)):
			a = words[i]
			if a in out: continue
			for j in range(i+1,len(words)):
				b = words[j]
				if b.startswith(a) and len(a)>=min_len:
					out[b] = a
				else:
					break
	return out

def set_adj_gender(word,g):
	w = word
	if g=='f':
		if w[-1] in ['i','y']:
			w = w[:-1]+u'a'
	elif g=='n':
		if w[-1]=='y':
			w = w[:-1]+u'e'
		elif w[-1]=='i':
			w = w+u'e'
	return w

def inf_to_noun(word):
	w = word
	if w.endswith(u'ać'):
		w = w[:-2]+u'anie'
	return w

def get_bigram_i_list(a,b):
	b1 = set([x-1 for x in b])
	return a&b1

def get_ngram_i_list(i_lists):
	out = set(i_lists[0])
	for n,i_list in enumerate(i_lists):
		if n==0: continue
		out &= set([i-n for i in i_list])
	return list(out)

# ------------------------------------------------------------------------------

def get_keywords(text,db):
	raw_tokens = re.findall(r'[\w\d-]+|[.?!-()\[\]:]',text,re.U)
	tokens,aux = analyze(raw_tokens,db,['lem','pos','name','phrase','gender','case'])
	out = [] # (score,w_cnt,token,i_list)
	if 1: # phrases
		max_i = len(tokens)
		i_list = aux['lem_i_list']
		score = {}
		for k,cnt in sorted(aux['phr'].items()):
			i_factor = 1.0*(max_i - min([min(i_list.get(x)) for x in k if i_list.get(x)]))/max_i
			cnt_factor = 1.0 * cnt
			len_factor = 1.0 * len(k)
			_score = i_factor * cnt_factor * len_factor
			score[k] = _score
			#print(u' '.join(k).encode('utf8'),_score,cnt,[list(i_list.get(x,[])) for x in k])
		for k,_score in sorted(score.items(),key=lambda x:x[1],reverse=True):
			rec_i_list = [list(i_list.get(w,[])) for w in k]
			rec_i_list = get_ngram_i_list(rec_i_list)
			rec = _score, len(k), u' '.join(k), rec_i_list
			out.append(rec)
	if 1: # words
		STOPWORDS = set(['to','do','po',u'niektóry','soba','jeden','co','wiele','bez','nasze','inny'])
		i_list = aux['lem_i_list']
		max_i = len(tokens)
		score = {}
		for t in tokens:
			x = t.lem
			if x in score: continue
			if t.pos != 'subst' and not t.name: continue
			if len(i_list[x])==1 and not t.name: continue
			if x in STOPWORDS: continue
			i_factor = 1.0*(max_i-min(i_list[x])) / max_i
			cnt_factor = 1.0*len(i_list[x]) + int(x[0].isupper()) + int(x[-1].isupper())
			score[x] = i_factor * cnt_factor
		for k,v in sorted(score.items(),key=lambda x:x[1],reverse=True):
			# print(k.encode('utf8'), v, list(i_list[k]))
			rec = v,1,k,list(i_list[k])
			out.append(rec)
	out.sort(reverse=True)
	return out

# ------------------------------------------------------------------------------

def run_sandbox(text,db):
	raw_tokens = re.findall(r'[\w\d-]+|[.?!-()\[\]:]',text,re.U)
	tokens,aux = analyze(raw_tokens,db,['lem','pos','name','phrase','gender','case'])
	if 1:
		for t in tokens:
			#if 'loc' in t._case:
			if t.pos in ['subst','adj']:
			#if ('subst' in t._pos or 'adj' in t._pos) and len(t._pos)==1:
			#if 'subst' in t._pos or 'adj' in t._pos:
				print(t.i, t.text.encode('utf8'), t.lem.encode('utf8'), t.pos, t.gender, t._gender, t._lem, t._pos, t._case, t.name, t.capital, t.all_caps, t.begin)
			else:
				#print(t.i, t.text.encode('utf8'))
				print(t.i, t.text.encode('utf8'), t.lem.encode('utf8'), t.pos, t.gender, t._gender, t._lem, t._pos, t._case, t.name, t.capital, t.all_caps, t.begin)
	print(len(raw_tokens),len(tokens))
	if 1:
		print(':'*80)
		max_i = len(tokens)
		i_list = aux['lem_i_list']
		score = {}
		for k,cnt in sorted(aux['phr'].items()):
			i_factor = 1.0*(max_i - min([min(i_list.get(x)) for x in k if i_list.get(x)]))/max_i
			cnt_factor = 1.0 * cnt
			len_factor = 1.0 * len(k)
			_score = i_factor * cnt_factor * len_factor
			score[k] = _score
			print(u' '.join(k).encode('utf8'),_score,cnt,[list(i_list.get(x,[])) for x in k])
		print(':'*40)
		for k,_score in sorted(score.items(),key=lambda x:x[1],reverse=True):
			print(u' '.join(k).encode('utf8'),_score)
	if 1:
		print('*'*80)
		for k,v in aux['ood'].most_common():
			print(k.encode('utf8'),v)
	if 1:
		print('*'*80)
		for k,v in aux['ood_lem'].items():
			print(k.encode('utf8'),'-->',v.encode('utf8'))
	if 0:
		print('*'*80)
		i_list = aux['lem_i_list']
		for t in tokens:
			print(t.i,t.lem.encode('utf8'),i_list[t.lem])
	if 1:
		print('='*80)
		STOPWORDS = set(['to','do','po',u'niektóry','soba','jeden','co','wiele','bez','nasze','inny'])
		i_list = aux['lem_i_list']
		max_i = len(tokens)
		score = {}
		for t in tokens:
			x = t.lem
			if x in score: continue
			if t.pos != 'subst' and not t.name: continue
			if len(i_list[x])==1 and not t.name: continue
			if x in STOPWORDS: continue
			i_factor = 1.0*(max_i-min(i_list[x])) / max_i
			cnt_factor = 1.0*len(i_list[x]) + int(x[0].isupper()) + int(x[-1].isupper())
			score[x] = i_factor * cnt_factor
		for k,v in sorted(score.items(),key=lambda x:x[1],reverse=True):
			print(k.encode('utf8'), v, list(i_list[k]))
	print(aux['t'])

	# if 0:
		# # bi
		# bi_cnt = Counter()
		# for w1,w2 in zip(lem_tokens,lem_tokens[1:]):
			# bi_cnt[w1,w2] += 1
		# STOP = [u'się',u'być','nie','nic','jak','gdy']
		# for x,c in bi_cnt.most_common():
			# if c==1:
				# words = x.split(' ')
				# upper = sum([int(t[0].isupper()) for t in words])
				# if len(words) < upper: continue
			# if len(x[0])<3 or len(x[1])<3: continue
			# if x[0] in STOP or x[1] in STOP: continue
			# print(x,c)

if __name__=="__main__":
	db = sqlite3.connect('multi8.sqlite')
	#
	import corpus
	text = corpus.text13
	#text = "ciemny niebieski niebo ciemny niebieski niebo"
	#
	#run_sandbox(text,db)
	kw_list = get_keywords(text,db)
	for k in kw_list:
		print(k[0],k[1],k[2].encode('utf8'),k[3])

# TODO BUG brakujace i_list po uzgadnianiu
# TODO POMYSL lematy uzywamy tylko do statystyk, jako output wybieramy cos z tresci lub cos co jest prefixem przy odmianie
# TODO holow-ać przyczepa -> holow-anie przyczepy (dopelniacz) -> przypadek z tekstu
# TODO hamow-ać silnik -> hamow-anie silnikiem (??) -> przypadek z tekstu
# TODO zmiana zmiana bieg, podczas podczas jazda
# TODO mąka -> mąka (nazwisko)
# TODO France -> franca
# TODO jesli wszystkie wystapienia w jednej formie to to jest lem? tylko dla nazw? -> przycisk hold
# TODO trzewiczek -> brak w slowniku jako nazwiska, wszystkie duze w tekscie
# TODO robert -> roberta (imie f)
# TODO benjamin -> imie,nazwisko
# TODO Nissan
# TODO obr./min
# TODO siemianowice śląskich -> śląskich brakuje w słowniku ???
# TODO dostały -> lem_cnt[.decode] ???
# TODO list gonczy
# TODO filtrowanie tylko gdy nie jest to jedyna opcja
# TODO Miał vs mieć (czasownik akurat bardziej popularny)
# TODO obrażenia vs obrażenie (brak bonusu)
# TODO temu vs to
