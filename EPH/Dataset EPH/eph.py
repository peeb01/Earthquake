import pandas as pd


df1 = pd.read_csv('D:\\Earthquake\\EPH\\Dataset EPH\\SUN_positions.csv')
df2 = pd.read_csv('D:\\Earthquake\\EPH\\Dataset EPH\\MERCURY BARYCENTER_positions.csv')
df3 = pd.read_csv('D:\\Earthquake\\EPH\\Dataset EPH\\VENUS BARYCENTER_positions.csv')
df4 = pd.read_csv('D:\\Earthquake\\EPH\\Dataset EPH\\MOON_positions.csv')
df5 = pd.read_csv('D:\\Earthquake\\EPH\\Dataset EPH\\MARS BARYCENTER_positions.csv')
df6 = pd.read_csv('D:\\Earthquake\\EPH\\Dataset EPH\\SATURN BARYCENTER_positions.csv')
df7 = pd.read_csv('D:\\Earthquake\\EPH\\Dataset EPH\\JUPITER BARYCENTER_positions.csv')
df8 = pd.read_csv('D:\\Earthquake\\EPH\\Dataset EPH\\URANUS BARYCENTER_positions.csv')
df9 = pd.read_csv('D:\\Earthquake\\EPH\\Dataset EPH\\NEPTUNE BARYCENTER_positions.csv')


column = ['SUN', 'MERCURY', 'VENUS', 'MOON', 'MARS', 'SATURN', 'JUPITER', 'URANUS', 'NEPTUNE']
pos = ['x',' y', 'z']
col = ['time'] + [f'{column[i]}_{pos[j]}' for i in range(len(column)) for j in range(len(pos))]



dfs = [df1, df2, df3, df4, df5, df6, df7, df8, df9]

result = pd.concat([df.set_index('time') for df in dfs], axis=1).reset_index().values
result = pd.DataFrame(result, columns = col)


dataset = pd.read_csv('D:\\Earthquake\\DataSet\\DATASET.csv')

dft = pd.concat([dataset[dataset['time'] == result['time']], result], axis=1)


dft.to_csv('Earthquake_Position_planets.csv')
print(result)