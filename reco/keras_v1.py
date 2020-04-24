import pandas as pd
from keras.layers import Embedding
from keras.layers import Input
from keras.layers import Dense
from keras.layers import Concatenate
from keras.layers import Dropout
from keras.layers import Flatten
from keras.models import Model
from keras.models import Sequential
import keras

df1 = pd.read_csv('ml-100k/u1.base',sep='\t',header=0,names=['user','movie','rating','ts'])
df2  = pd.read_csv('ml-100k/u1.test',sep='\t',header=0,names=['user','movie','rating','ts'])

ui = Input(shape=(1,),name='user')
ue = Embedding(1000,150)(ui)
uf = Flatten()(ue)
mi = Input(shape=(1,),name='movie')
me = Embedding(1700,150)(mi)
mf = Flatten()(me)
merged = Concatenate()([uf,mf])
h1 = Dense(100,activation='relu')(merged)
h1d = Dropout(0.25)(h1)
h2 = Dense(200,activation='relu')(h1d)
h2d = Dropout(0.5)(h2)
h3 = Dense(300,activation='relu')(h2)
out = Dense(1,activation='sigmoid')(h3)

model = Model(inputs=[ui,mi],outputs=out)
print(model.summary())
#model.compile(optimizer='adam',loss='binary_crossentropy',metrics=['binary_accuracy'])
model.compile(optimizer='adam',loss='mse',metrics=['binary_accuracy'])

x1 = df1['user']
x2 = df1['movie']
y = df1.from_dict({'rating':map(int,df1['rating']>=4)})

model.fit({'user':x1,'movie':x2},y)

# TODO f1
# TODO roc
