import numpy as np
import pandas as pd
from tensorflow.keras import layers, models, Input, Model
from sklearn.model_selection import train_test_split
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

# df_pacific = df1

x = df_pacific.iloc[:, 4:-2].drop_duplicates()
x = x.values.astype('float32')

y_latitude = df_pacific.groupby(['date', 'latitude'])['val'].sum().unstack().reset_index().fillna(0).set_index('date')
y_latitude = y_latitude.values.astype('float32')

y_longitude = df_pacific.groupby(['date', 'longitude'])['val'].sum().unstack().reset_index().fillna(0).set_index('date')
y_longitude = y_longitude.values.astype('float32')


x_train, x_val, y_latitude_train, y_latitude_val = train_test_split(x, y_latitude, test_size=0.2, shuffle=False)
_, _, y_longitude_train, y_longitude_val = train_test_split(x, y_longitude, test_size=0.2, shuffle=False)

input_shape = x_train.shape[1]
input_layer = Input(shape=(input_shape,))

print(x.shape)
print(y_latitude.shape)
print(y_longitude.shape)

shared = layers.Dense(units=64, activation='relu')(input_layer)
shared = layers.Dense(units=128, activation='relu')(shared)


latitude_output = layers.Dense(units=64, activation='relu')(shared)
latitude_output = layers.Dense(units=y_latitude.shape[1], activation='softmax')(latitude_output)

longitude_output = layers.Dense(units=64, activation='relu')(shared)
longitude_output = layers.Dense(units=128, activation='relu')(longitude_output)
longitude_output = layers.Dense(units=48, activation='relu')(longitude_output)


longitude_output = layers.Dense(units=y_longitude.shape[1], activation='softmax')(longitude_output)

model = Model(inputs=input_layer, outputs=[latitude_output, longitude_output])

model.compile(optimizer='adam',
              loss=['mse', 'mse'],
              metrics=['accuracy'])

model.fit(
    x_train, 
    [y_latitude_train, y_longitude_train], 
    epochs=2000, 
    batch_size=16, 
    validation_data=(x_val, [y_latitude_val, y_longitude_val])
)

model.save('ModelTraining/ANNpyALL.h5')

loss, latitude_loss, longitude_loss, latitude_acc, longitude_acc = model.evaluate(x, [y_latitude, y_longitude])
print(f"\nOverall loss: {loss}")
print(f"Latitude loss: {latitude_loss}, Latitude accuracy: {latitude_acc}")
print(f"Longitude loss: {longitude_loss}, Longitude accuracy: {longitude_acc}")