import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


df = pd.read_csv('D:\Project\Senior-Project-Earthquake-Prediction\DataSet\DATASET.csv')
df['time'] = pd.to_datetime(df['time'], errors='coerce')
df['time'] = df['time'].dt.strftime("%Y-%m-%d %H:%M")

#neo 
neo = pd.read_csv('D:/Project/Senior-Project-Earthquake-Prediction/NEOsDataset/NEOsq10LDto2050.csv')
neo['cd'] = pd.to_datetime(neo['cd'], format="%Y-%b-%d %H:%M")
neo['cd'] = neo['cd'].dt.strftime("%Y-%m-%d %H:%M")


ndt = df[['time','latitude','longitude','mag','depth']]
# at Thailand   ---(ndt['mag']>=3) &
ndt = ndt[(ndt['latitude']<= 20.920) &(ndt['latitude']>=5.6400) & (ndt['longitude']>=96) & (ndt['longitude']<=107)]


ndt['time'] = pd.to_datetime(ndt['time'])

fig = plt.figure()
ax = fig.add_subplot(projection='3d')

formatted_time = ndt['time'].dt.strftime('%Y')

ax.scatter(ndt['longitude'], ndt['time'].astype('int64'), ndt['latitude'], marker='o')
ax.set_xlabel('Latitude')
ax.set_ylabel('Time')  
ax.set_zlabel('Longitude')


ax.set_yticklabels(formatted_time)

plt.show()