
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

df = pd.read_csv('D:\Project\Earthquake\DataSet\DATASET.csv')

df['time'] = pd.to_datetime(df['time'], errors='coerce')
df['time'] = df['time'].dt.strftime("%Y-%m-%d %H:%M")

ndt = df[['time', 'latitude', 'longitude', 'mag', 'depth']]
# at Thailand   ---(ndt['mag']>=3) &
# ndt = ndt[(ndt['mag'] >= 2) & (ndt['latitude'] <= 30.449) & (ndt['latitude'] >= -15.284) & (ndt['longitude'] >= 80.97) & (ndt['longitude'] <= 156.797)]       # SEA
# ndt = ndt[(ndt['mag']>=4) &(ndt['latitude']<= 20.920) &(ndt['latitude']>=5.6400) & (ndt['longitude']>=96) & (ndt['longitude']<=107)]                          # Thailand
ndt = ndt[(ndt['mag']>=4) &(ndt['latitude']<=  45.551483) &(ndt['latitude']>=24.396308) & (ndt['longitude']>=122.934570) & (ndt['longitude']<= 153.986672)]     # Japan
ndt['time'] = pd.to_datetime(ndt['time'])

fig, axs = plt.subplots(2, 1, figsize=(10, 8))
axs[0].scatter(ndt['time'], ndt['latitude'])
axs[1].scatter(ndt['time'], ndt['longitude'])
plt.show()
