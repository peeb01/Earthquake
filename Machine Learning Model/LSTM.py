import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import *
from keras.callbacks import ModelCheckpoint, EarlyStopping
from keras.losses import MeanSquaredError, MeanAbsoluteError
from keras.activations import *
from keras.metrics import RootMeanSquaredError
from keras.optimizers import Adam
from keras.models import load_model


DATA_PATH = "DATASET_STORE\\UPDATE DATASET_1.csv"
df = pd.read_csv(DATA_PATH)
df['datetime'] = pd.to_datetime(df['datetime'])
df1 = df[df['datetime']>= '1980-01-01 00:00:01']

df1['date'] = df1['datetime'].dt.date
df1['val'] = 1

df1 = df1[df1['mag'] >= 3]

df1['latitude'] = df1['latitude'].astype('int')
df1['longitude']= df1['longitude'].astype('int')


fillter = (df1['latitude'] >= -59.889) & (df1['latitude'] <= 65.026) & \
          ((df1['longitude'] >= 139.219) & (df1['longitude'] <= 267.188) | (df1['longitude'] >= -180) & (df1['longitude'] <= (-267.188+180))) & \
          (df1['datetime']>= '1980-01-01 00:00:01')

df_pacific = df1[fillter]       # This Union with Australia Plate and Califonia Plate and Nazaca Plate

# Remove Australia Plate
au_filter = ~(((df_pacific['latitude'] > -60) & (df_pacific['latitude']  < -19.83) & 
              (df_pacific['longitude'] > 139) & (df_pacific['longitude'] < 151.2)) |
              ((df_pacific['latitude'] > -40.5) & (df_pacific['latitude']  < -20) & 
              (df_pacific['longitude'] > 151) & (df_pacific['longitude'] < 161))  
             )
df_pacific = df_pacific[au_filter]

# Remove North America Plate and Eurasia Plate and Nazca Plate
na_filter = ~(
    ((df_pacific['latitude'] >= 61) & (df_pacific['latitude'] <= 65) & (df_pacific['longitude'] >= -135) & (df_pacific['longitude'] <= -87)) |
    ((df_pacific['latitude'] >= 54) & (df_pacific['latitude'] <= 57) & (df_pacific['longitude'] >= -122) & (df_pacific['longitude'] <= -115)) |
    ((df_pacific['latitude'] >= 37) & (df_pacific['latitude'] <= 47) & (df_pacific['longitude'] >= -115.5) & (df_pacific['longitude'] <= -87)) |
    ((df_pacific['latitude'] >= 31.6) & (df_pacific['latitude'] <= 37) & (df_pacific['longitude'] >= -112.5) & (df_pacific['longitude'] <= -95)) |
    ((df_pacific['latitude'] >= 27.5) & (df_pacific['latitude'] <= 30.5) & (df_pacific['longitude'] >= -109.2) & (df_pacific['longitude'] <= -89)) |
    ((df_pacific['latitude'] >= 14) & (df_pacific['latitude'] <= 23.1) & (df_pacific['longitude'] >= -100.5) & (df_pacific['longitude'] <= -87)) |
    ((df_pacific['latitude'] >= -1) & (df_pacific['latitude'] <= 14) & (df_pacific['longitude'] >= -99) & (df_pacific['longitude'] <= -87)) | 
    ((df_pacific['latitude'] >= -49) & (df_pacific['latitude'] <= -17) & (df_pacific['longitude'] >= -106.5) & (df_pacific['longitude'] <= -85)) | 
    ((df_pacific['latitude'] >= 58.3) & (df_pacific['latitude'] <= 66) & (df_pacific['longitude'] >= 140) & (df_pacific['longitude'] <= 180)) | 
    ((df_pacific['latitude'] >= 58.3) & (df_pacific['latitude'] <= 66) & (df_pacific['longitude'] >= -180) & (df_pacific['longitude'] <= -167)) |
    ((df_pacific['latitude'] >= 30) & (df_pacific['latitude'] <= 66) & (df_pacific['longitude'] >= -105) & (df_pacific['longitude'] <= 0))
)

df_pacific = df_pacific[na_filter]

latitude = df_pacific['latitude'].values.flatten()
longitude = df_pacific['longitude'].values.flatten()


def windows(df, window_size = 21):
    df_np = df
    x = []
    y = []
    for i in range(len(df_np)-window_size):
        row = [[a] for a in df_np[i:i+window_size]]
        x.append(row)
        label = df_np[i+window_size]
        y.append(label)
    return np.array(x), np.array(y)

WINDOWS_SIZE = 20

x_lat, y_lat = windows(latitude, WINDOWS_SIZE)
x_lon, y_lon = windows(longitude, WINDOWS_SIZE)


model_lat = Sequential()
model_lat.add(InputLayer((WINDOWS_SIZE,1)))
model_lat.add(LSTM(64))
model_lat.add(Dense(128, relu))
model_lat.add(Dense(1, linear))

patience = 2
early_stopping = EarlyStopping(monitor='val_loss', patience=patience, mode='min')
model_lat.compile(loss=MeanSquaredError(), optimizer=Adam())

model_lat.fit(x_lat, y_lat, epochs=10, callbacks=[early_stopping])
# IPython.display.clear_output()
model_lat.save('ModelTraining/latitude_lstm.h5')

pred = model_lat.predict(x_lat).flatten()
print(pred.shape)
print(y_lat.shape)
train_result = pd.DataFrame({'Pred': pred, 'Actual': y_lat.flatten()})

plt.plot(train_result['Actual'][-100:], label='Actual')
plt.plot(train_result['Pred'][-100:], label='Predict')
plt.show()