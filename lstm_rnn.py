import numpy as np 
import pandas as pd 
from matplotlib import pyplot as plt

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM

from sklearn.preprocessing import MinMaxScaler
min_max_scaler = MinMaxScaler()


class LSTM_RNN:
	def __init__(self, num_units, batch_size, num_epochs):
		self.num_units = num_units
		self.batch_size = batch_size
		self.num_epochs = num_epochs
	
	def train_model(self, x_train, y_train):
		activation_function = 'sigmoid'
		optimizer = 'adam'
		loss_function = 'mean_squared_error'

		# Initialize the RNN
		regressor = Sequential()

		# Adding the input layer and the LSTM layer
		regressor.add(LSTM(units = self.num_units, activation = activation_function, input_shape=(None, 1)))

		# Adding the output layer
		regressor.add(Dense(units = 1))

		# Compiling the RNN
		regressor.compile(optimizer = optimizer, loss = loss_function)

		# Using the training set to train the model
		history = regressor.fit(x_train, y_train, batch_size = self.batch_size, epochs = self.num_epochs)
		return (regressor, history)

	def predict(self, test_set, regressor):
		test_set = test_set.values


		inputs = np.reshape(test_set, (len(test_set), 1))
		inputs = min_max_scaler.fit_transform(inputs)
		inputs = np.reshape(inputs, (len(inputs), 1, 1))

		predicted_price = regressor.predict(inputs)
		predicted_price = min_max_scaler.inverse_transform(predicted_price)
		return (test_set, predicted_price)
