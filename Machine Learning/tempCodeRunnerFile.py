import tensorflow as tf
import pandas as pd
import matplotlib.pyplot as plt
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from keras.models import load_model

cwd = os.getcwd()
path = cwd + '\\DataSet\\DATASET.csv'

df = pd.read_csv(path)

ndt = df[['time', 'latitude', 'longitude']]
ndt['time'] = pd.to_datetime(ndt['time'])

ndt = ndt[(ndt['latitude'] <= 30.449) & (ndt['latitude'] >= -15.284) & (ndt['longitude'] >= 80.97) & (ndt['longitude'] <= 156.797)]
minla = min(ndt['latitude'])
minlo = min(ndt['longitude'])
maxla = max(ndt['latitude'])
maxlo = max(ndt['longitude'])


print(minla, minlo, maxla, maxlo)
