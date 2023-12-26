import os
import tensorflow as tf
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
from keras.models import load_model

cwd = os.getcwd()
path = cwd + '\\DataSet\\DATASET.csv'

df = pd.read_csv(path)

ndt = df[['time', 'latitude', 'longitude']]
ndt['time'] = pd.to_datetime(ndt['time'])

ndt = ndt[(ndt['latitude'] <= 30.449) & (ndt['latitude'] >= -15.284) & (ndt['longitude'] >= 80.97) & (ndt['longitude'] <= 156.797)]

ndt.loc[:, 'year'] = ndt['time'].dt.year
ndt.loc[:, 'month'] = ndt['time'].dt.month
ndt.loc[:, 'day'] = ndt['time'].dt.day
ndt.loc[:, 'hour'] = ndt['time'].dt.hour
ndt.loc[:, 'minute'] = ndt['time'].dt.minute
ndt.loc[:, 'second'] = ndt['time'].dt.second

ndt = ndt.drop(columns=['time'])
ndt = ndt[['year','month','day','hour','minute','second','latitude', 'longitude']]

scaler = MinMaxScaler()
ndt[['latitude', 'longitude']] = scaler.fit_transform(ndt[['latitude', 'longitude']])

train, test_validate = train_test_split(ndt, test_size=0.3, random_state=42)
test, validate = train_test_split(test_validate, test_size=0.5, random_state=42)



model = load_model(cwd + '\my_model.h5')

predictions = model.predict(test[['year', 'month', 'day', 'hour', 'minute', 'second']])

plt.scatter(test['year'], predictions[:, 0], label='Predicted Latitude', alpha=0.5)
plt.scatter(test['year'], test['latitude'], label='Actual Latitude', alpha=0.5)
plt.scatter(test['year'], predictions[:, 1], label='Predicted Longitude', alpha=0.5)
plt.scatter(test['year'], test['longitude'], label='Actual Longitude', alpha=0.5)
plt.title('Actual vs Predicted Latitude, Longitude')
plt.xlabel('Actual Year')
plt.ylabel('Latitude, Longitude')
plt.legend()
plt.show()
