import tensorflow as tf
import pandas as pd
import matplotlib.pyplot as plt
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from keras.models import load_model

cwd = os.getcwd()
path = cwd + '\\DataSet\\DATASET.csv'

df = pd.read_csv(path)

ndt = df[['time', 'latitude', 'longitude']]
ndt['time'] = pd.to_datetime(ndt['time'])

ndt = ndt[(ndt['latitude'] <= 30.449) & (ndt['latitude'] >= -15.284) & (ndt['longitude'] >= 80.97) & (ndt['longitude'] <= 156.797)]
minla = min(ndt['latitude'])
minlo = min(ndt['longitude'])
maxla = max(ndt['latitude'])
maxlo = max(ndt['longitude'])


print(minla, minlo, maxla, maxlo)

# Convert the 'time' column to Unix timestamp (seconds since epoch)
ndt['timestamp'] = ndt['time'].astype('int64') / 10**15

ndt = ndt.drop(columns=['time'])

ndt = ndt[['timestamp', 'latitude', 'longitude']]

scaler = MinMaxScaler()
ndt[['latitude', 'longitude']] = scaler.fit_transform(ndt[['latitude', 'longitude']])



train, test_validate = train_test_split(ndt, test_size=0.3, random_state=42)
test, validate = train_test_split(test_validate, test_size=0.5, random_state=42)

# Assuming your model architecture
model = load_model(cwd + '\my_model.h5')

# Predictions
predictions = model.predict(test[['timestamp']])
# original_values = scaler.inverse_transform(predictions)
# predictions = original_values
print(predictions)

# Plotting Latitude
plt.plot(test['timestamp'], predictions[:, 0], label='Predicted Latitude', alpha=0.5)
plt.plot(test['timestamp'], test['latitude'], label='Actual Latitude', alpha=0.5)
plt.plot(test['timestamp'], predictions[:, 1], label='Predicted Longitude', alpha=0.5)
plt.plot(test['timestamp'], test['longitude'], label='Actual Longitude', alpha=0.5)
plt.title('Actual vs Predicted Latitude, Longitude')
plt.xlabel('Actual Timestamp')
plt.ylabel('Latitude, longitude')
plt.legend()
plt.show()

# Plotting Longitude

# plt.title('Actual vs Predicted Longitude')
# plt.xlabel('Actual Timestamp')
# plt.ylabel('Longitude')
# plt.legend()
# plt.show()
