import pandas as pd

df = pd.read_csv('D:\Project\Earthquake\Comets\data0.csv')

print(df)
df_pivoted = df.pivot(index='Time', columns='Object', values=['X', 'Y', 'Z'])

df_pivoted.columns = [f'{col[1]}_{col[0]}' for col in df_pivoted.columns]

df_pivoted.reset_index(inplace=True)

print(df_pivoted)