from request_data import request_data
from push_to_bucket import push_to_bucket
from process_data import process_data
from predict_SVM import *
from linear_regression import *

import pandas as pd


request     = request_data(limit=1950, date=1362960000, stop=100)
exchange    = request.data("daily_exchange")
price       = request.data("price")

data     = pd.concat([price, exchange], axis=1)

columns = ['open', 'volume']
df_data = request.select_columns(data, columns)

acc_linear = linear_reg(df_data) 
test_model(df_data)
acc_scv    = predict_svm(df_data)

aws_s3 = push_to_bucket()
aws_s3.create_bucket("ykuqergjer")
aws_s3.push_to_bucket(bucket="forecastbitcoinresult", filename="correct.txt")

