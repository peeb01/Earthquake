import pandas as pd


eph = pd.read_csv('POST.csv')
df = pd.read_csv('UPDATE_EARTHQUAKE.csv')
df['datetime'] = df['time']

df['time'] = pd.to_datetime(df['time'])
df['time'] = df['time'].dt.strftime('%Y-%m-%d')
eph['time'] = pd.to_datetime(eph['time'])
eph['time'] = eph['time'].dt.strftime('%Y-%m-%d')

merged_df = pd.merge(df, eph, on='time', how='inner')
print(merged_df.iloc[:, 5:])