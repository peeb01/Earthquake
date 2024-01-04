#Updates


import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

df = pd.read_csv('D:\Project\Earthquake\DataSet\DATASET.csv')

df['time'] = pd.to_datetime(df['time'], errors='coerce')
df['time'] = df['time'].dt.strftime("%Y-%m-%d %H:%M")

#neo 
# neo = pd.read_csv('D:/Project/Senior-Project-Earthquake-Prediction/NEOsDataset/NEOsq10LDto2050.csv')
# neo['cd'] = pd.to_datetime(neo['cd'], format="%Y-%b-%d %H:%M")
# neo['cd'] = neo['cd'].dt.strftime("%Y-%m-%d %H:%M")


ndt = df[['time','latitude','longitude','mag','depth']]
# at Thailand   ---(ndt['mag']>=3) &
ndt = ndt[(ndt['mag']>=2) & (ndt['latitude']<= 30.449) &(ndt['latitude']>=-15.284) & (ndt['longitude']>=80.97) & (ndt['longitude']<=156.797)]
# ndt = ndt[(ndt['mag']>=4) &(ndt['latitude']<= 20.920) &(ndt['latitude']>=5.6400) & (ndt['longitude']>=96) & (ndt['longitude']<=107)]

print(len(ndt))
print(ndt.describe().transpose())

ndt['time'] = pd.to_datetime(ndt['time'])

min_year = ndt['time'].dt.year.min()
max_year = ndt['time'].dt.year.max()
equally_spaced_years = np.linspace(min_year, max_year, max_year - min_year + 1)

# fig = plt.figure()
# ax = fig.add_subplot(projection='3d')

# ax.scatter(ndt['longitude'], ndt['time'].dt.year, ndt['latitude'], marker='^')

# ax.set_xlabel('Longitude')
# ax.set_ylabel('Time')  
# ax.set_zlabel('Latitude')

# ax.set_yticks(equally_spaced_years)
# ax.set_yticklabels([str(int(year)) for year in equally_spaced_years])

# plt.show()


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
