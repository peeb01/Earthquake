# Standart Library
import os

# 3rd Party Library
import tensorflow as tf
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt

# Project Library

cwd = os.getcwd()
path = cwd + '\\DataSet\\DATASET.csv'

df = pd.read_csv(path)

ndt = df[['time', 'latitude', 'longitude']]
ndt['time'] = pd.to_datetime(ndt['time'])

ndt = ndt[(ndt['latitude'] <= 30.449) & (ndt['latitude'] >= -15.284) & (ndt['longitude'] >= 80.97) & (ndt['longitude'] <= 156.797)]

ndt.loc[:, 'year'] = ndt['time'].dt.year
ndt.loc[:, 'month'] = ndt['time'].dt.month
ndt.loc[:, 'day'] = ndt['time'].dt.day
ndt.loc[:, 'hour'] = ndt['time'].dt.hour
ndt.loc[:, 'minute'] = ndt['time'].dt.minute
ndt.loc[:, 'second'] = ndt['time'].dt.second

ndt = ndt.drop(columns=['time'])


ndt = ndt[['year','month','day','hour','minute','second','latitude', 'longitude']]
print(ndt.head())

