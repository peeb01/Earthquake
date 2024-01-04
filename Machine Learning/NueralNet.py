import os
import tensorflow as tf
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

cwd = os.getcwd()
path = cwd + '\\DataSet\\DATASET.csv'

df = pd.read_csv(path)

ndt = df[['time', 'latitude', 'longitude']]
ndt = ndt[(ndt['latitude'] <= 30.449) & (ndt['latitude'] >= -15.284) & (ndt['longitude'] >= 80.97) & (ndt['longitude'] <= 156.797)]

ndt['time'] = pd.to_datetime(ndt['time'], format='%Y-%m-%d %H:%M:%S')
ndt['time'] = ndt['time'].apply(pd.Timestamp.timestamp)





ndt = ndt[['time', 'latitude', 'longitude']]


scaler = MinMaxScaler()
ndt[['latitude', 'longitude']] = scaler.fit_transform(ndt[['latitude', 'longitude']])

train, test_validate = train_test_split(ndt, train_size=0.7, random_state=42)
test, validate = train_test_split(test_validate, train_size=0.67, random_state=42)


model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Dense(16, input_dim=1, activation = tf.keras.activations.relu)) 
model.add(tf.keras.layers.Dense(32, activation = tf.keras.activations.relu))
model.add(tf.keras.layers.Dense(64, activation = tf.keras.activations.relu))
model.add(tf.keras.layers.Dense(32, activation = tf.keras.activations.relu))
model.add(tf.keras.layers.Dense(2, activation = tf.keras.activations.softmax))  

model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mse'])

model.fit(train[['time']], train[['latitude', 'longitude']], epochs=5, batch_size=32, validation_data=(validate[['time']], validate[['latitude', 'longitude']]))

test_loss, test_mse = model.evaluate(test[['time']], test[['latitude', 'longitude']])

model.save('timestamp_my_model.h5')

print(f"Test Loss: {test_loss}, Test MSE: {test_mse}")

print(f"Test Loss: {test_loss}, Test MSE: {test_mse}")

predictions = model.predict(test[['time']])

fig, axs = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

axs[0].scatter(test['time'], predictions[:, 0], label='Predicted Latitude', alpha=0.5)
axs[0].scatter(test['time'], test['latitude'], label='Actual Latitude', alpha=0.5)
axs[0].set_ylabel('Latitude')
axs[0].legend()

axs[1].scatter(test['time'], predictions[:, 1], label='Predicted Longitude', alpha=0.5)
axs[1].scatter(test['time'], test['longitude'], label='Actual Longitude', alpha=0.5)
axs[1].set_xlabel('Time')
axs[1].set_ylabel('Longitude')
axs[1].legend()

fig.suptitle('Actual vs Predicted Latitude, Longitude')
plt.show()