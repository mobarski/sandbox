# code from: https://towardsdatascience.com/build-an-extreme-learning-machine-in-python-91d1e8958599
# data from: https://www.kaggle.com/oddrationale/mnist-in-csv
from time import time
t0=time()

hidden_size = 1000 # 2k:80,72  1k:28,21  500:16,8

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
from scipy.linalg import pinv2

train = pd.read_csv('mnist_train.csv')
test = pd.read_csv('mnist_test.csv')

t1 = time()

onehotencoder = OneHotEncoder(categories='auto')
scaler = MinMaxScaler()
#scaler = StandardScaler()

X_train = scaler.fit_transform(train.values[:,1:])
y_train = onehotencoder.fit_transform(train.values[:,:1]).toarray()
X_test = scaler.fit_transform(test.values[:,1:])
y_test = onehotencoder.fit_transform(test.values[:,:1]).toarray()

input_size = X_train.shape[1]
print('X_train.shape',X_train.shape)
print('y_train.shape',y_train.shape)

input_weights = np.random.normal(size=[input_size,hidden_size])
biases = np.random.normal(size=[hidden_size])

def relu(x):
	return np.maximum(x, 0, x)

def hidden_nodes(X):
	G = np.dot(X, input_weights)
	G = G + biases
	H = relu(G)
	return H

output_weights = np.dot(pinv2(hidden_nodes(X_train)), y_train)

def predict(X):
	out = hidden_nodes(X)
	out = np.dot(out, output_weights)
	return out

prediction = predict(X_test)
correct = 0
total = X_test.shape[0]

for i in range(total):
	predicted = np.argmax(prediction[i])
	actual = np.argmax(y_test[i])
	correct += 1 if predicted == actual else 0
accuracy = correct/total
print('Accuracy for ', hidden_size, ' hidden nodes: ', accuracy)

print(time()-t0)
print(time()-t1)

