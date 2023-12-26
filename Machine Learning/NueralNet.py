# Standart Library
import os

# 3rd Party Library
import tensorflow as tf
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt

# Project Library



cwd = os.getcwd()
path = cwd + '\\DataSet\\DATASET.csv'

df = pd.read_csv(path)

ndt = df[['time', 'latitude', 'longitude']]
ndt['time'] = pd.to_datetime(ndt['time'])

ndt = ndt[(ndt['latitude'] <= 30.449) & (ndt['latitude'] >= -15.284) & (ndt['longitude'] >= 80.97) & (ndt['longitude'] <= 156.797)]

ndt['year'] = ndt['time'].dt.year
ndt['month'] = ndt['time'].dt.month
ndt['day'] = ndt['time'].dt.day
ndt['hour'] = ndt['time'].dt.hour
ndt['minute'] = ndt['time'].dt.minute
ndt['second'] = ndt['time'].dt.second


ndt['timestamp'] = ndt['time']

ndt = ndt.drop(columns=['time'])

ndt = ndt[['year','month','day','hour','minute','second','latitude', 'longitude']]

# print(ndt.shape)
# print(ndt.head())

scaler = MinMaxScaler()
ndt[['latitude', 'longitude']] = scaler.fit_transform(ndt[['latitude', 'longitude']])

train, test_validate = train_test_split(ndt, test_size=0.3, random_state=42)
test, validate = train_test_split(test_validate, test_size=0.5, random_state=42)


model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Dense(16, input_dim=6, activation = tf.keras.activations.softmax)) 
model.add(tf.keras.layers.Dense(32, activation = tf.keras.activations.softmax))
model.add(tf.keras.layers.Dense(64, activation = tf.keras.activations.softmax))
model.add(tf.keras.layers.Dense(32, activation = tf.keras.activations.softmax))
model.add(tf.keras.layers.Dense(2, activation = tf.keras.activations.softmax))  

model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mae'])

model.fit(train[['year','month','day','hour','minute','second']], train[['latitude', 'longitude']], epochs=50, batch_size=32, validation_data=(validate[['year','month','day','hour','minute','second']], validate[['latitude', 'longitude']]))

test_loss, test_mae = model.evaluate(test[['year','month','day','hour','minute','second']], test[['latitude', 'longitude']])

print(f"Test Loss: {test_loss}, Test MAE: {test_mae}")
model.save('my_model.h5')
print(f"Test Loss: {test_loss}, Test MAE: {test_mae}")

predictions = model.predict(test[['timestamp', 'latitude', 'longitude']])

plt.plot(test['timestamp'], predictions[:, 0], label='Predicted Latitude', alpha=0.5)
plt.plot(test['timestamp'], test['latitude'], label='Actual Latitude', alpha=0.5)
plt.plot(test['timestamp'], predictions[:, 1], label='Predicted Longitude', alpha=0.5)
plt.plot(test['timestamp'], test['longitude'], label='Actual Longitude', alpha=0.5)
plt.title('Actual vs Predicted Latitude, Longitude')
plt.xlabel('Actual Timestamp')
plt.ylabel('Latitude, longitude')
plt.legend()
plt.show()