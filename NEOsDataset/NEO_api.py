"""
API column name from : https://ssd-api.jpl.nasa.gov/doc/cad.html 

"""


import requests
import pandas as pd

src = 'https://ssd-api.jpl.nasa.gov/cad.api?dist-max=10LD&date-min=1950-01-01&date-max=2050-01-01&sort=dist'

data = requests.get(src)

data = data.json()

# print(data)
# print('\t'.join(data['fields']))
# for row in data['data']:
#     print('\t'.join(row))
# print(data)
header = data['fields']
rows = data['data']

df = pd.DataFrame(rows, columns=header)
csv_filename = 'NEOsq10LDto2050.csv'
df.to_csv(csv_filename, index=False)
