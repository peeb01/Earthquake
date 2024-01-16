import pandas as pd
import numpy as np



df = pd.read_csv('D:\Project\Earthquake\Comets\\raw_asteroid\AsteroidPositionFinal.csv')

# print(df[['Time', 'X', 'Y', 'Z']])


# print(df)

object_planet = ['SUN', '199', '299', '399', '301', '599', '699', '433', 'Eros', 'Orus', '90000188', '90000190', '90000191', 
                        'Leucus', 'Eurybates','Polymele', 'Vesta', 'Mathilde', 'Lutetia', 'Donaldjohanson','Braille', 'Annefrank', 
                        'Bennu', 'Itokawa', 'Apophis', 'Ryugu', '-122911', 'Patroclus', 
                        '90000855', 'Dinkinesh','Gaspra', 'Ceres']



print(print(len(object_planet)*3))

