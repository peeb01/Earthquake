import tensorflow as tf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


path = 'D:\DataSet\DATASET_UPDATE_TO_ML.csv'

df = pd.read_csv(path)


print(df.head(10))