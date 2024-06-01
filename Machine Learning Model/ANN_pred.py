import numpy as np
import pandas as pd
from tensorflow.keras import layers, models, Input, Model
from sklearn.model_selection import train_test_split
from keras.models import load_model

import warnings
warnings.filterwarnings("ignore")


DATA_PATH = "DATASET_STORE\\UPDATE DATASET_1.csv"
df = pd.read_csv(DATA_PATH)
df['datetime'] = pd.to_datetime(df['datetime'])
df1 = df[df['datetime']>= '1980-01-01 00:00:01']

df1['date'] = df1['datetime'].dt.date
df1['val'] = 1

df1 = df1[df1['mag'] >= 7]

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

xe = df_pacific.drop_duplicates(subset=['date'])
x = xe.iloc[:, 4:-2]
x = x.values.astype('float32')

y_latitude = xe.groupby(['date', 'latitude'])['val'].sum().unstack().reset_index().fillna(0).set_index('date')
lat_col = y_latitude.columns
y_latitude = y_latitude.values.astype('float32')

y_longitude = xe.groupby(['date', 'longitude'])['val'].sum().unstack().reset_index().fillna(0).set_index('date')
lon_col = y_longitude.columns
y_longitude = y_longitude.values.astype('float32')


x_train, x_val, y_latitude_train, y_latitude_val = train_test_split(x, y_latitude, test_size=0.2, shuffle=False)
_, _, y_longitude_train, y_longitude_val = train_test_split(x, y_longitude, test_size=0.2, shuffle=False)


model = load_model('ModelTraining\ANNpyALL.h5')

pred = model.predict(x_train)
# print(pred)

lati = pd.DataFrame(pred[0], columns=lat_col)
long = pd.DataFrame(pred[1], columns=lon_col)

latitude = []
longitude = []
act_lat = []
act_lon = []

for i in range(len(lati)):
    for j in range(len(lati.iloc[i, :])):
        if lati.iloc[i, j] == np.max(lati.iloc[i, :]):
            latitude.append(lat_col[j])

for i in range(len(long)):
    for j in range(len(long.iloc[i, :])):
        if long.iloc[i, j] == np.max(long.iloc[i, :]):
            longitude.append(lon_col[j])

for i in range(len(y_latitude_train)):
    for j in range(len(y_latitude_train[i, :])):
        if y_latitude_train[i, j] == np.max(y_latitude_train[i, :]):
            act_lat.append(lat_col[j])

for i in range(len(y_longitude_train)):
    for j in range(len(y_longitude_train[i, :])):
        if y_longitude_train[i, j] == np.max(y_longitude_train[i, :]):
            act_lon.append(lon_col[j])

# print(len(latitude))
# print(len(longitude))
# print(len(act_lat))
# print(len(act_lon))

# print(x_train.shape)
# print(y_latitude.shape)
# print(y_longitude.shape)

ndf = pd.DataFrame({
    "Actual latitude": act_lat,
    "Actual lonngitude": act_lon,
    "Latitude" : latitude,
    "Longitude": longitude
})

print(ndf)
ndf.to_csv("Data Testing/ANNtrain.csv", index=False)