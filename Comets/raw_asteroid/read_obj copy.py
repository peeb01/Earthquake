import pandas as pd
import numpy as np



df = pd.read_csv('D:\Project\Earthquake\Comets\\raw_asteroid\AsteroidPositionFinal1.csv')

# print(df[['Time', 'X', 'Y', 'Z']])


# print(df)

object_planet = ['SUN', '199', '299', '399', '301', '599', '699', '433', 'Eros', 'Orus', '90000188', '90000190', '90000191', 
                        'Leucus', 'Eurybates','Polymele', 'Vesta', 'Mathilde', 'Lutetia', 'Donaldjohanson','Braille', 'Annefrank', 
                        'Bennu', 'Itokawa', 'Apophis', 'Ryugu', '-122911', 'Patroclus', 
                        '90000855', 'Dinkinesh','Gaspra', 'Ceres']



print(print(len(object_planet)*3))


df['time'] = pd.to_datetime(df['Time'])
df1 = df[['time','Object_Name', 'X', 'Y', 'Z']]
a = df[['X', 'Y', 'Z']].values.tolist()

ls = []
for i in range(len(df1)):
    ls += a[i]

columns = 96

_2d_list = [ls[i:i+columns] for i in range(0, len(ls), columns)]

lis = pd.DataFrame(_2d_list).astype(str)

time = pd.read_csv('D:\Project\Earthquake\Comets\\time.csv')
time = pd.to_datetime(time['Date'])
time = time[time >= '2000-01-01']

time.reset_index(drop=True, inplace=True)
lis.reset_index(drop=True, inplace=True)

data = pd.concat([time, lis], axis=1)

columns = ['Time'] + [f'{obj}_{coord}' for obj in object_planet for coord in ['X', 'Y', 'Z']]

data.columns = columns

data.to_csv('ASTroidCTrain.csv', index=False)