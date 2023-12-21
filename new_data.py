import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import os

cwd = os.getcwd()
datapath = cwd + "\\DataSet\\DATASET.csv"


df = pd.read_csv(datapath)
df = pd.read_csv(datapath)
df['time'] = pd.to_datetime(df['time'], errors='coerce')
dt_time = df['time'].dt.strftime("%Y-%m-%d %H:%M")
df['time'] = df['time'].dt.strftime("%Y-%m-%d")

neopath = os.getcwd() + "\\NEOsDataset\\NEOsq10LDto2050.csv"
neo = pd.read_csv(neopath)
neo['cd'] = pd.to_datetime(neo['cd'], format="%Y-%b-%d %H:%M")
neo_time = neo['cd'].dt.strftime("%Y-%m-%d %H:%M")
neo['cd'] = neo['cd'].dt.strftime("%Y-%m-%d")

print(df.head())
print('------------------------')
print(neo.head())

print(dt_time.head())
print(neo_time.head())

columname = ['time','latitude','longitude','mag','depth', 'dist', 'dist_min', 'dist_max']
arr = []



