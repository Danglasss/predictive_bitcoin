from request_data import request_data
from lstm_rnn import LSTM_RNN

import pandas as pd
import matplotlib.pyplot as plt


request = request_data(limit=2000, date=1362960000, stop=100)
data    = request.data("price")

columns = ['open']
df_data = request.select_columns(data, columns)

x_train, y_train, test_set, train_set = request.get_set(df_data) 


modele                     = LSTM_RNN(num_units=4, batch_size=5, num_epochs=4)
regressor, history         = modele.train_model(x_train, y_train)

plt.plot(history.history['loss'])

test_set, predicted_price  = modele.predict(test_set, regressor)


plt.figure(figsize=(25, 25), dpi=80, facecolor = 'w', edgecolor = 'k')

plt.plot(test_set[:, 0], color='red', label='Real BTC Price')
plt.plot(predicted_price[:, 0], color = 'blue', label = 'Predicted BTC Price')

plt.title('BTC Price Prediction', fontsize = 40)
plt.xlabel('Time', fontsize=40)
plt.ylabel('BTC Price(USD)', fontsize = 40)
plt.legend(loc = 'best')
plt.show()
