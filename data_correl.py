import numpy as np
import pandas as pd

path = 'D:\DataSet\DATASET_UPDATE_TO_ML.csv'
df = pd.read_csv(path)

x = df.iloc[:, 5:].values
lat = df['latitude'].values
lon = df['longitude'].values
mag = df['mag'].values

correl = []

for i in range(len(x[0])):
    lat_corr = np.corrcoef(lat, x[:, i])[0, 1]
    lon_corr = np.corrcoef(lon, x[:, i])[0, 1]
    mag_corr = np.corrcoef(mag, x[:, i])[0, 1]
    correl.append(lat_corr)
    correl.append(lon_corr)
    correl.append(mag_corr)


correl = np.array(correl)


for row in correl:
    print(row)
    if row >= 0.45:
        print(f'HIGH {row}')



