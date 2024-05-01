from skyfield.api import load, Topos
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

eph = load('de421.bsp')

list_eph = ['SUN', 'MERCURY BARYCENTER', 'VENUS BARYCENTER', 'MOON', 'MARS', 'JUPITER BARYCENTER', 'SATURN BARYCENTER', 'URANUS BARYCENTER', 'NEPTUNE BARYCENTER']

start_date = datetime(1950, 9, 23)
end_date = datetime(2024, 2, 21)
delta = timedelta(days=1)  
date_range = pd.date_range(start_date, end_date, freq=delta)

columns = ['DateTime']
for body_name in list_eph:
    columns.extend([f"{body_name}_x", f"{body_name}_y", f"{body_name}_z", f"distance_{body_name.lower()}"])
df = pd.DataFrame(columns=columns)

ts = load.timescale()
for date_time in date_range:
    t = ts.utc(date_time.year, date_time.month, date_time.day)
    row_data = [date_time]
    for body_name in list_eph:
        body = eph[body_name]
        astrometric = body.at(t)
        x, y, z = astrometric.position.au - eph['earth'].at(t).position.au
        row_data.extend([x, y, z])
        distance = np.linalg.norm([x, y, z])
        row_data.append(distance)
    df.loc[len(df)] = row_data

df.to_csv('celestial_positions_with_distances.csv', index=False)
