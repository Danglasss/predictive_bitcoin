import requests
import pandas as pd
from datetime import datetime
from datetime import timedelta
import matplotlib.pyplot as plt

class request_data:
	
	def __init__(self, limit, date):
		self.limit = limit
		
		# API key
		self.apiKey = "2f89100faea89908b275fc72a8543be88f0b977697e1919f74d47dd705f4e6dc"
		
		# link to get data in a dict :
		self.dict = dict()
		self.dict["daily_exchange"] = "https://min-api.cryptocompare.com/data/exchange/histoday"
		self.dict["price"] = "https://min-api.cryptocompare.com/data/v2/histoday"

		#  Timestamp of today 
		today_date = datetime.now().timestamp()
		self.timestamp = int(today_date)
	
		# Value of 1 day convert in timestamp
		self.oneday = 86400

		# date of data extraction (Bitcoin launch date == (1297036800))
		self.date = date

	def __request_data(self, key):
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
		while self.date < self.timestamp:
			df = self.__request_data(key)
			stack_df = self.__time_travel(key, df, stack_df)
		if key == "price":
			stack_df = pd.DataFrame(list(stack_df))
		return (stack_df)

request = request_data(limit=2000, date=1297036800)
daily_exchange = request.data("daily_exchange")
#daily_exchange = request.data("price")

with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    print(daily_exchange)
exit(1)


daily_exchange.plot(x ='time', y=['high', 'low'])
plt.show()
