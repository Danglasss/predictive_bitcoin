import requests
import pandas as pd
from datetime import datetime
from datetime import timedelta
import matplotlib.pyplot as plt

class request_data:
	
	def __init__(self, limit):
		self.limit = limit
		
		# API key
		self.apiKey = "2f89100faea89908b275fc72a8543be88f0b977697e1919f74d47dd705f4e6dc"
		
		# link to get data in a dict :
		self.dict = dict()
		self.dict["daily_exchange"] = "https://min-api.cryptocompare.com/data/exchange/histoday"
		self.dict["price"] = "https://min-api.cryptocompare.com/data/v2/histoday"

		#  Timestamp of today 
		date = datetime.now().timestamp()
		self.timestamp = int(date)
	
		# Value of 1 day in timestamp
		self.oneday = 86400

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
		result = result['Data']
		return (result)

	def __concat_df(self, df, stack_df):
		if stack_df is not 0:
			stack_df = pd.concat(([df, stack_df]), ignore_index = True)
		else :
			stack_df = df
		return (stack_df)

	def data(self, key):
		stack_df = 0
		# Bitcoin launch date == (1297036800)
		while 1297036800 < self.timestamp:
			df = self.__request_data(key)
			self.timestamp = df[0]["time"] - self.oneday
			stack_df = self.__concat_df(df, stack_df)
		return (list(stack_df))


request = request_data(2000)
daily_exchange = request.data("price")
daily_exchange = pd.DataFrame(daily_exchange)


with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    print(daily_exchange)


daily_exchange.plot(x ='time', y=['high', 'low'])
plt.show()
