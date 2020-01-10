
def setup_encoder(text,inputs):
	global chars,len_chars,c_to_i,i_to_c,INPUTS
	INPUTS = inputs
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

#INPUTS = 4

def get_xy(sentences):
	x = np.zeros((len(sentences),INPUTS,len_chars),dtype='b')
	y = np.zeros((len(sentences),len_chars),dtype='b')
	for i,text in enumerate(sentences):
		x[i]=text_to_hot(text[:-1])
		y[i]=text_to_hot(text[-1:])[0]
	return x,y
	
# if 0:
	# sentences = [text[i:i+INPUTS+1] for i in range(len(text)-INPUTS-1)]
	# x,y = get_xy(sentences)
	# print(x)
	# print(y)

# ------------------------------------------------------------------------------

from keras.models import Sequential,load_model
from keras.layers import Dense,LSTM
from keras.optimizers import RMSprop

def get_model(units,rate=0.1):
	model = Sequential()
	model.add(LSTM(units, input_shape=(INPUTS,len_chars)))
	model.add(Dense(len_chars,activation='softmax'))
	optimizer=RMSprop(learning_rate=rate)
	model.compile(optimizer,loss='categorical_crossentropy')
	return model

# if 1:
	# model = get_model(4)
	# model.fit(x,y,batch_size=3,epochs=20)
	# model.save('lstm_my.h5')
# else:
	# model = load_model('lstm_my.h5')

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

def generate(model,text,size,t=1.0):
	assert len(text)==INPUTS
	out = text[:]
	for j in range(size):
		x = np.array([text_to_hot(text)])
		py = model.predict(x)[0]
		pc=i_to_c[sample(py,t)]
		out = out + pc
		text = out[-INPUTS:]
	return out
