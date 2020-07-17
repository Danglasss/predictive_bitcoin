import numpy as np
import pickle

class process_data:
	def __init__(self, df_data):
		self.df_data = df_data

	def get_class_y(self, x_data, y_data):
		Y = np.zeros((y_data.size, 1))
		i = 0
		for i, (x, y) in enumerate(zip(x_data, y_data)):
			if y > x:
				Y[i] = 1
		return (Y)

	def data_classifier(self, y_key, classifier, prediction_day):
		X = self.df_data[0:len(self.df_data) - prediction_day]
		Y = self.df_data[prediction_day:len(self.df_data)]
		Y = Y[y_key]
		if classifier == True:
			Y = self.get_class_y(X[y_key], Y)
		return X, Y
	
	def save_model(self, filename, model):
		filename = filename + ".pickle"
		with open(filename, "wb") as f:
			pickle.dump(model, f)

	def load_model(self, filename):
		filename = filename + ".pickle"
		f = open(filename, "rb")
		model = pickle.load(f)
		return model
