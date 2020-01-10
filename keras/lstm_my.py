text = """
ala ma kota
a kot ma ale
"""

# ------------------------------------------------------------------------------

# TODO as class

chars = list(sorted(set(text))) # stabilne indeksy
len_chars = len(chars)+1
c_to_i = {c:i+1 for i,c in enumerate(chars)}
i_to_c = {i+1:c for i,c in enumerate(chars)}

def text_to_i(text):
	return [c_to_i.get(c,0) for c in text]

def text_to_hot(text):
	out = [[0]*len_chars for _ in text]
	i_list = text_to_i(text)
	for n,i in enumerate(i_list):
		out[n][i] = 1
	return out

# ------------------------------------------------------------------------------

import numpy as np

INPUT = 4

sentences = [text[i:i+INPUT+1] for i in range(len(text)-INPUT-1)]
x = np.zeros((len(sentences),INPUT,len_chars),dtype='b')
y = np.zeros((len(sentences),len_chars),dtype='b')
for i,text in enumerate(sentences):
	x[i]=text_to_hot(text[:-1])
	y[i]=text_to_hot(text[-1:])[0]

print(x)
print(y)

# ------------------------------------------------------------------------------

from keras.models import Sequential,load_model
from keras.layers import Dense,LSTM
from keras.optimizers import RMSprop

if 0:
	model = Sequential()
	model.add(LSTM(4, input_shape=(INPUT,len_chars)))
	#model.add(LSTM(4, batch_input_shape=(3,INPUT,len_chars), stateful=True))
	model.add(Dense(len_chars,activation='softmax'))

	optimizer=RMSprop(learning_rate=0.1)
	model.compile(optimizer,loss='categorical_crossentropy')
	model.fit(x,y,batch_size=3,epochs=20)
	model.save('lstm_my.h5')
else:
	model = load_model('lstm_my.h5')

# ------------------------------------------------------------------------------

def sample(p_list, t=1.0):
	if not t: return np.argmax(p_list)
	p_list = p_list.astype('float64') # bez tego suma norm_p moze byc > 1
	log_p = np.log(p_list) / t
	exp_p = np.exp(log_p)
	norm_p = exp_p / np.sum(exp_p)
	results = np.random.multinomial(1, norm_p, 1)
	return np.argmax(results)

# ------------------------------------------------------------------------------

if 0:
	px = np.array([text_to_hot('kot')])
	py = model.predict(px)

	pi=sample(py,0)
	pc=i_to_c[pi]

	print(px)
	print(py)
	print(i_to_c)
	print(pi)
	print(pc)

# ------------------------------------------------------------------------------

# TODO function

text = 'ala '
out = text[:]
for j in range(20):
	x = np.array([text_to_hot(text)])
	py = model.predict(x)[0]
	pc=i_to_c[sample(py,1.0)]
	out = out + pc
	text = out[-INPUT:]
print(out)
