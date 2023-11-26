#Updates


import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

df = pd.read_csv('D:\Project\Senior-Project-Earthquake-Prediction\DataSet\DATASET.csv')
df['time'] = pd.to_datetime(df['time'], errors='coerce')
df['time'] = df['time'].dt.strftime("%Y-%m-%d %H:%M")

#neo 
neo = pd.read_csv('D:/Project/Senior-Project-Earthquake-Prediction/NEOsDataset/NEOsq10LDto2050.csv')
neo['cd'] = pd.to_datetime(neo['cd'], format="%Y-%b-%d %H:%M")
neo['cd'] = neo['cd'].dt.strftime("%Y-%m-%d %H:%M")


ndt = df[['time','latitude','longitude','mag','depth']]
# at Thailand   ---(ndt['mag']>=3) &
#ndt = ndt[(ndt['mag']>=6) & (ndt['latitude']<= 30.449) &(ndt['latitude']>=-15.284) & (ndt['longitude']>=80.97) & (ndt['longitude']<=156.797)]
ndt = ndt[(ndt['mag']>=4) &(ndt['latitude']<= 20.920) &(ndt['latitude']>=5.6400) & (ndt['longitude']>=96) & (ndt['longitude']<=107)]


ndt['time'] = pd.to_datetime(ndt['time'])


min_year = ndt['time'].dt.year.min()
max_year = ndt['time'].dt.year.max()
equally_spaced_years = np.linspace(min_year, max_year, max_year - min_year + 1)


fig = plt.figure()
ax = fig.add_subplot(projection='3d')


ax.scatter(ndt['longitude'], ndt['time'].dt.year, ndt['latitude'], marker='o')

ax.set_xlabel('Longitude')
ax.set_ylabel('Time')  
ax.set_zlabel('Latitude')


ax.set_yticks(equally_spaced_years)
ax.set_yticklabels([str(int(year)) for year in equally_spaced_years])

plt.show()