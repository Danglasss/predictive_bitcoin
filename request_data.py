import requests
import pandas as pd
from datetime import datetime
from datetime import timedelta
import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import MinMaxScaler
min_max_scaler = MinMaxScaler()
from datetime import datetime


class request_data:
	
	def __init__(self, limit, date, stop):
		self.limit = limit
		self.apiKey = "2f89100faea89908b275fc72a8543be88f0b977697e1919f74d47dd705f4e6dc"
		
		# date of data extraction ([11 mars 2013] == (1362960000))
		self.date = date

		# link to get data in a dict :
		self.dict = dict()
		self.dict["daily_exchange"] = "https://min-api.cryptocompare.com/data/exchange/histoday"
		self.dict["price"] = "https://min-api.cryptocompare.com/data/v2/histoday"

		#  Timestamp of today 
		today_date = datetime.now().timestamp()
		self.timestamp = int(today_date)

		# Value of 1 day convert in timestamp
		self.oneday = 86400

		# value of stop
		self.stop = stop

	def __request_data(self, key):
		"""
			Make request to get data from URL; 
			Some params : (limit = number of data requested)
						  (Timestamp = The date which we start to recover the data)
		"""
		url = self.dict[key]
		payload = {
    		"api_key": self.apiKey,
    		"fsym": "BTC",
    		"tsym": "USD",
    		"limit": self.limit,
    		"toTs": self.timestamp
		}
		result = requests.get(url, params=payload).json()
		result = pd.DataFrame(result['Data'])
		return (result)

	def __concat_df(self, df, stack_df):
		if stack_df is not 0:
			stack_df = pd.concat(([df, stack_df]), ignore_index = True)
		else :
			stack_df = df
		return (stack_df)

	def __time_travel(self, key, df, stack_df):
		"""
			Take the next value of "self.timestamp"
			Concat the dataframe 
		"""
		if key == "price":
			self.timestamp = df['Data'][0]["time"] - self.oneday
			df = df['Data']
			stack_df = self.__concat_df(df, stack_df)
		if key == "daily_exchange":
			self.timestamp = df["time"][0] - self.oneday
			stack_df = self.__concat_df(df, stack_df)
		return (stack_df)
	
	def data(self, key):
		stack_df = 0
		index    = 0
		while self.date < self.timestamp and index < self.stop:
			df = self.__request_data(key)
			stack_df = self.__time_travel(key, df, stack_df)
			index += 1
		if key == "price":
			stack_df = pd.DataFrame(list(stack_df))
		return (stack_df)

	def select_columns(self, data, columns):
		# convert timestamp to date an add column date
		data['date'] = pd.to_datetime(data['time'],unit='s').dt.date
		
		# Séléctionner et réarranger les colonnes
		data = data[columns]
		return (data)

	def get_set(self, data):
		"""
			Get train_set and test_set | cut it into X, Y
		"""
		prediction_days = 7
		train_set = data[:len(data)-prediction_days]
		test_set  = data[len(data)-prediction_days:]

		training_set = train_set.values
		training_set = min_max_scaler.fit_transform(training_set)

		x_train = training_set[0:len(training_set)-1]
		y_train = training_set[1:len(training_set)]
		x_train = np.reshape(x_train, (len(x_train), 1, 1))
		return (x_train, y_train, test_set, train_set) 
