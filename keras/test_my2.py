from lstm_my2 import setup_encoder,get_xy,get_model,sample,generate,load_model

text = """
ala ma kota
a kot ma ale
"""
text = open('gh3v2.txt').read(2048).lower()

INPUTS = 20
setup_encoder(text,INPUTS)

if 0:
	LSTM_UNITS = 30
	EPOCHS = 40
	BATCH = 100
	#
	sentences = [text[i:i+INPUTS+1] for i in range(len(text)-INPUTS-1)]
	x,y = get_xy(sentences)
	model = get_model(LSTM_UNITS,rate=0.05)
	model.fit(x,y,batch_size=BATCH,epochs=EPOCHS)
	model.save('lstm_my2.h5')
else:
	model = load_model('lstm_my2.h5')

print(generate(model,' '*INPUTS,2048,0.5))
