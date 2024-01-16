import pandas as pd


df1 = pd.read_csv('D:\Project\Earthquake\Comets\Concat1.csv')
df2 = pd.read_csv('D:\Project\Earthquake\Comets\Concat2.csv')
df3 = pd.read_csv('D:\Project\Earthquake\Comets\Concat3.csv')
df4 = pd.read_csv('D:\Project\Earthquake\Comets\Concat4.csv')
df5 = pd.read_csv('D:\Project\Earthquake\Comets\Concat5.csv')
df6 = pd.read_csv('D:\Project\Earthquake\Comets\Concat6.csv')
df7 = pd.read_csv('D:\Project\Earthquake\Comets\Concat7.csv')
df8 = pd.read_csv('D:\Project\Earthquake\Comets\Concat8.csv')

new_df = pd.concat([df1, df2, df3, df4, df5, df6, df7, df8], ignore_index=True)

new_df.to_csv('AllAsteroid.csv', index=False)
