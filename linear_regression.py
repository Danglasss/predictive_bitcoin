from process_data import process_data
from process_data import process_data
import sklearn
from sklearn import linear_model

import matplotlib.pyplot as plt

from sklearn import preprocessing
max_abs_scaler = preprocessing.MaxAbsScaler()


def test_model(df_data):
	process = process_data(df_data)
	X, Y = process.data_classifier(y_key="open", classifier=False, prediction_day=7)
	
	Linear = process.load_model("linear_predict_7")
	prediction = Linear.predict(X)

	#plt.style.use("ggplot")
	plt.scatter(X["volume"], df_data["timestamp"],  color='black')
	#plt.plot(X["volume"], prediction, color='blue', linewidth=3)

	plt.xticks(())
	plt.yticks(())

	plt.show()

def linear_reg(df_data):
	process = process_data(df_data)

	X, Y = process.data_classifier(y_key="open", classifier=False, prediction_day=7)
	best = 0
	for i in range(30):
		x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(X, Y, test_size=0.01)

		Linear = linear_model.LinearRegression()
		Linear.fit(x_train, y_train.ravel())
		acc = Linear.score(x_test, y_test.ravel())

		if acc > best:
			best = acc
			process.save_model("linear_predict_7", Linear)
		if best > 0.8:
			break 

	return (acc)
