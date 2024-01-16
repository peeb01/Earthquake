import re
import pandas as pd
from threading import Thread


from astropy.coordinates import SkyCoord
from astropy.time import Time
from astroquery.jplhorizons import Horizons


# # list object
# object_plannet = ['SUN', '199', '299', '399', '301', '-74', '599', '699', '433', 'Eros', 'Orus', '-49',
#                        '-490', '-255', '2000016', '90000190',  
#                         'Leucus', 'Eurybates','Polymele', 'Vesta', 'Mathilde', 'Lutetia', 'Donaldjohanson','Braille', 'Annefrank', 
#                         'Bennu', 'Itokawa', '-64', 'Apophis', 'Ryugu', '-122911', 'Patroclus', 
#                         '90000855', 'Dinkinesh', '20065803' , 'Gaspra', 'Ceres']

# def calculate_position(obj, time):
#     """
#     Args : 
#         obj     : obj name str
#         time    : time (utc) format yyyy-mm-dd
#     """
#     epoch = Time(time)
#     q = Horizons(obj, location='@0', epochs=epoch.tdb.jd)
#     tab = q.vectors(refplane='earth')
#     c = SkyCoord(tab['x'].quantity, tab['y'].quantity, tab['z'].quantity,
#                 representation_type='cartesian', frame='icrs',
#                 obstime=epoch)
#     result = str(c)
#     matches = re.findall(r'-?\d+\.\d+', result)
#     result_list = [float(match) for match in matches]
#     return result_list

import pandas as pd
time = pd.read_csv('D:\Project\Earthquake\Comets\\time.csv')
time['time'] = pd.to_datetime(time['Date'])
time = time[time['time'] >= '2000-01-01'].astype(str)
time = time['time']
print(len(time))

from functon import PositionCalculator

calculator = PositionCalculator()

data = calculator.positions_parallel(time[:1000])
data.to_csv('data0.csv')

print(data)


data = calculator.positions_parallel(time[1000:2000])
data.to_csv('data1.csv')

print(data)



data = calculator.positions_parallel(time[2000:3000])
data.to_csv('data2.csv')

print(data)



data = calculator.positions_parallel(time[3000:4000])
data.to_csv('data3.csv')

print(data)



data = calculator.positions_parallel(time[4000:5000])
data.to_csv('data4.csv')

print(data)


data = calculator.positions_parallel(time[5000:6000])
data.to_csv('data5.csv')

print(data)



data = calculator.positions_parallel(time[6000:7000])
data.to_csv('data6.csv')

print(data)


data = calculator.positions_parallel(time[7000:])
data.to_csv('data7.csv')

print(data)
