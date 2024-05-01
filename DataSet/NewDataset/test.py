import pandas as pd

df1 = pd.read_csv('DATASET_UPDATE.csv')
df2 = pd.read_csv('qu.csv')



df2['time'] = pd.to_datetime(df2['time'])
df1['time'] = pd.to_datetime(df1['time'])
df1['time'] = df1['time'].dt.strftime('%Y-%m-%d %H:%M:%S')
df2['time'] = df2['time'].dt.strftime('%Y-%m-%d %H:%M:%S')

print(df1.head())
print(df2.head())

df2 = df2[['time', 'latitude', 'longitude', 'mag', 'depth']]
df = pd.concat([df1, df2])
df.to_csv('UPDATE_EARTHQUAKE.csv', index=False)