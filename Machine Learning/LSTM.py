import os

import numpy as np
import tensorflow as tf
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import LSTM, Dense




cwd = os.getcwd()
path = cwd + '\\DataSet\\DATASET.csv'

df = pd.read_csv(path)

ndt = df[['time','latitude', 'longitude']]

ndt = ndt[(ndt['latitude'] <= 30.449) & (ndt['latitude'] >= -15.284) & (ndt['longitude'] >= 80.97) & (ndt['longitude'] <= 156.797)]

date_time = pd.to_datetime(ndt.pop('time'), format='%Y-%m-%d %H:%M:%S')
timestamp_s = date_time.map(pd.Timestamp.timestamp)


day = 24*60*60
year = (365.2425)*day

ndt['Day sin'] = np.sin(timestamp_s * (2 * np.pi / day))
ndt['Day cos'] = np.cos(timestamp_s * (2 * np.pi / day))
ndt['Year sin'] = np.sin(timestamp_s * (2 * np.pi / year))
ndt['Year cos'] = np.cos(timestamp_s * (2 * np.pi / year))


# ndt = ndt.drop(columns=['time'])
# ndt = ndt[['year','month','day','hour','minute','second','latitude', 'longitude']]

scaler = MinMaxScaler()
ndt[['latitude', 'longitude']] = scaler.fit_transform(ndt[['latitude', 'longitude']])

train, test_validate = train_test_split(ndt, test_size=0.2, random_state=42)
test, validate = train_test_split(test_validate, test_size=0.5, random_state=42)

n_steps = 8

model = Sequential()
model.add(LSTM(50, activation='relu', input_shape=(n_steps, 1)))
model.add(Dense(1))
model.compile(optimizer='adam', loss='mse') 

model.fit(X_train, y_train, epochs=500, batch_size=32)

train_predictions = model.predict(X_train)
test_predictions = model.predict(X_test)

model.save("AQI_time_series_model.h5")


plt.figure(figsize=(12, 6))
plt.plot(df['NO'], df['AQI'], label='Actual', color='blue')
plt.plot(np.arange(n_steps, len(train_predictions) + n_steps), train_predictions, label='Training Predictions', linestyle='dashed', color='orange')
plt.plot(np.arange(len(df) - len(test_predictions), len(df)), test_predictions, label='Testing Predictions', linestyle='dashed', color='green')

plt.title('Time Series Prediction')
plt.xlabel('Time Step')
plt.ylabel('AQI')
plt.legend()
plt.savefig('training')
plt.show()
