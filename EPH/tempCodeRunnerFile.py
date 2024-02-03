from skyfield.api import load, Topos
import pandas as pd


df = pd.read_csv('D:\Earthquake\DataSet\DATASET.csv')
df['time'] = pd.to_datetime(df['time'])
df['y'] = df['time'].dt.year
df['m'] = df['time'].dt.month
df['d'] = df['time'].dt.day
df['h'] = df['time'].dt.hour
df['mm'] = df['time'].dt.minute
df['s'] = df['time'].dt.second

print(df.head())
