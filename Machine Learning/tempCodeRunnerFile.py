import os
import tensorflow as tf
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt


cwd = os.getcwd()
path = cwd + '\\DataSet\\DATASET.csv'

df = pd.read_csv(path)

ndt = df[['time', 'latitude', 'longitude']]
ndt = ndt[(ndt['latitude'] <= 30.449) & (ndt['latitude'] >= -15.284) & (ndt['longitude'] >= 80.97) & (ndt['longitude'] <= 156.797)]

ndt['time'] = pd.to_datetime(ndt['time'], format='%Y-%m-%d %H:%M:%S')
ndt['time'] = ndt.map(pd.Timestamp.timestamp)

ndt = ndt[['time','latitude', 'longitude']]
