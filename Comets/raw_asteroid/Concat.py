import pandas as pd

df1 = pd.read_csv('D:\Project\Earthquake\Comets\\raw_asteroid\data0.csv')
df2 = pd.read_csv('D:\Project\Earthquake\Comets\\raw_asteroid\data1.csv')
df3 = pd.read_csv('D:\Project\Earthquake\Comets\\raw_asteroid\data2.csv')
df4 = pd.read_csv('D:\Project\Earthquake\Comets\\raw_asteroid\data3.csv')
df5 = pd.read_csv('D:\Project\Earthquake\Comets\\raw_asteroid\data4.csv')
df6 = pd.read_csv('D:\Project\Earthquake\Comets\\raw_asteroid\data5.csv')
df7 = pd.read_csv('D:\Project\Earthquake\Comets\\raw_asteroid\data6.csv')
df8 = pd.read_csv('D:\Project\Earthquake\Comets\\raw_asteroid\data7.csv')


new_df = pd.concat([df1, df2, df3, df4, df5, df6, df7, df8], ignore_index=True)
new_df.to_csv('RAW_DATA_ASTEROIDS.csv')
