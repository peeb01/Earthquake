import pandas as pd
import numpy as np
from keras.models import load_model
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import plotly.express as px 


epoch = int(input("Enter Epochs : "))

df = pd.read_csv('D:\Senior Project\Earthquake\Machine Learning Model\DATASET_STORE\pacific.csv')

data = df[['latitude', 'longitude', 'SUN_x', 'SUN_y', 'SUN_z', 'distance_sun',
           'MERCURY BARYCENTER_x', 'MERCURY BARYCENTER_y', 'MERCURY BARYCENTER_z', 'distance_mercury barycenter',
           'VENUS BARYCENTER_x', 'VENUS BARYCENTER_y', 'VENUS BARYCENTER_z', 'distance_venus barycenter',
           'MOON_x', 'MOON_y', 'MOON_z', 'distance_moon', 'MARS_x', 'MARS_y', 'MARS_z', 'distance_mars',
           'JUPITER BARYCENTER_x', 'JUPITER BARYCENTER_y', 'JUPITER BARYCENTER_z', 'distance_jupiter barycenter',
           'SATURN BARYCENTER_x', 'SATURN BARYCENTER_y', 'SATURN BARYCENTER_z', 'distance_saturn barycenter',
           'URANUS BARYCENTER_x', 'URANUS BARYCENTER_y', 'URANUS BARYCENTER_z', 'distance_uranus barycenter',
           'NEPTUNE BARYCENTER_x', 'NEPTUNE BARYCENTER_y', 'NEPTUNE BARYCENTER_z', 'distance_neptune barycenter']]

data = data.values

scaler_features = MinMaxScaler()
scaler_targets = MinMaxScaler()

scaler_features.fit(data[:, :2])
scaler_targets.fit(data[:, :2])

data[:, :2] = scaler_features.transform(data[:, :2])


time_steps = 10  
num_features = data.shape[1]

# time steps and features
time_steps = 10 
num_features = data.shape[1]

sequences = []
targets = []
for i in range(len(data) - time_steps):
    sequences.append(data[i:i+time_steps])
    targets.append(data[i+time_steps, 0:2])  # Predict latitude and longitude

sequences = np.array(sequences)
targets = np.array(targets)

X_train, X_temp, y_train, y_temp = train_test_split(sequences, targets, test_size=0.3, shuffle=False)
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.66, shuffle=False)

model = load_model('D:\Senior Project\Earthquake\Machine Learning Model\ModelTraining\Pacific_DATA_training.h5')


model.fit(X_train, y_train, validation_data=(X_val, y_val), epochs=epoch, batch_size=32)

model.save('D:\Senior Project\Earthquake\Machine Learning Model\ModelTraining\Pacific_DATA_training.h5')

predictions = model.predict(X_test)
predictions = scaler_targets.inverse_transform(predictions)
targets_original = scaler_targets.inverse_transform(targets)

plt.figure(figsize=(14, 6))

plt.subplot(1, 2, 1)
plt.plot(predictions[-100:, 0], label='Predicted Latitude')
plt.plot(targets_original[-100:, 0], label='Actual Latitude')
plt.title('Predicted vs Actual Latitude')
plt.xlabel('n')
plt.ylabel('Latitude')
plt.legend()


plt.subplot(1, 2, 2)
plt.plot(predictions[-100:, 1], label='Predicted Longitude')
plt.plot(targets_original[-100:, 1], label='Actual Longitude')
plt.title('Predicted vs Actual Longitude')
plt.xlabel('n')
plt.ylabel('Longitude')
plt.legend()

plt.tight_layout()
plt.show()


geo_data = pd.DataFrame({
            "latitude"  : predictions[:, 0],
            "longitude" : predictions[:, 1]
})

actual_data = pd.DataFrame({
    "latitude" : targets_original[:, 0],
    "longitude": targets_original[:, 1]
})

geo_plot = geo_data.iloc[-500:, :]
actual_plot = actual_data.iloc[-500:, :]


geo_plot['source'] = 'predicted'
actual_plot['source'] = 'actual'

combined_data = pd.concat([geo_plot, actual_plot])

fig = px.scatter_geo(combined_data,
                     lat="latitude",
                     lon="longitude",
                     color="source",
                     title="Earthquake Position",
                     category_orders={"source": ["predicted", "actual"]})

fig.update_layout(height=500, width=800)

fig.show()