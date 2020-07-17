import requests
import pandas as pd
from datetime import datetime
from datetime import timedelta
import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from datetime import datetime
from sklearn import preprocessing
import json
import time

max_abs_scaler = preprocessing.MaxAbsScaler()

class request_data:
	
	def __init__(self, limit, date, stop):
		self.limit = limit
		self.apiKey = "2f89100faea89908b275fc72a8543be88f0b977697e1919f74d47dd705f4e6dc"
		self.apiKey = "cc239fb5d177f7a441fec899bec9e8821eddbd6e6cbbf47e4554012bd3bfd7e0"
		# date of data extraction ([11 mars 2013] == (1362960000))
		self.date = date

		# link to get data in a dict :
		self.dict = dict()
		self.dict["daily_exchange"] = "https://min-api.cryptocompare.com/data/exchange/histoday"
		self.dict["price"] = "https://min-api.cryptocompare.com/data/v2/histoday"

		#  Timestamp of today 
		self.today_date = datetime.now().timestamp()
		self.timestamp  = int(self.today_date)

		# Value of 1 day convert in timestamp
		self.oneday = 86400

		# value of stop
		self.stop = stop

	def request_data_(self, key):
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
		try :
			result = requests.get(url, params=payload).json()
		except :
			print("Can't scrap with cryptocompare")
			exit(1)
		result = pd.DataFrame(result['Data'])
		return (result)

	def concat_df_(self, df, stack_df):
		if stack_df is not 0:
			stack_df = pd.concat(([df, stack_df]), ignore_index = True)
		else :
			stack_df = df
		return (stack_df)

	def time_travel_(self, key, df, stack_df):
		"""
			Take the next value of "self.timestamp"
			Concat the dataframe 
		"""
		if key == "price":
			self.timestamp = df['Data'][0]["time"] - self.oneday
			stack_df = self.concat_df_(df['Data'], stack_df)
		if key == "daily_exchange":
			self.timestamp = df["time"][0] - self.oneday
			stack_df = self.concat_df_(df, stack_df)
		return (stack_df)
	
	def resize_df_(self, key, stack_df):
		if key == "price":
			stack_df = pd.DataFrame(list(stack_df))
		if key == "daily_exchange":
			stack_df = stack_df["volume"]
		return (stack_df)

	def data(self, key):
		stack_df = 0
		index    = 0
		while self.date < self.timestamp and index < self.stop:
			df       = self.request_data_(key)
			stack_df = self.time_travel_(key, df, stack_df)
			index    += 1
		stack_df = self.resize_df_(key, stack_df)
		self.timestamp = int(self.today_date)
		return (stack_df)

	def select_columns(self, data, columns):
		"""
			convert timestamp to date an add column date
			select all the value since the 11 mars 2013
			Séléctionner et réarranger les colonnes
		"""

		data['date'] = pd.to_datetime(data['time'],unit='s').dt.date
		data = data[data.time > 1362873600]
		data = data[columns]

		return (data)
