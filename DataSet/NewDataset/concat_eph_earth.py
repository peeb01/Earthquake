import pandas as pd


eph = pd.read_csv('POST.csv')
df = pd.read_csv('UPDATE_EARTHQUAKE.csv')
df['datetime'] = df['time']

df['time'] = pd.to_datetime(df['time'])
df['time'] = df['time'].dt.strftime('%Y-%m-%d')
eph['time'] = pd.to_datetime(eph['time'])
eph['time'] = eph['time'].dt.strftime('%Y-%m-%d')

merged_df = pd.merge(df, eph, on='time', how='inner')
# print(merged_df.iloc[:, 5:])

new_df = pd.concat([merged_df.iloc[:, 5], merged_df.iloc[:, 1:4], merged_df.iloc[:, 6:]], axis=1)
print(new_df)

new_df.to_csv('UPDATE DATASET_1.csv', index=False)