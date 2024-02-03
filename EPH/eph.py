import pandas as pd
import concurrent.futures
from skyfield.api import load, Topos
import numpy as np

def calculate_sun_position(row):
    t = ts.utc(year=row['y'], month=row['m'], day=row['d'], hour=row['h'], minute=row['mm'], second=row['s'])
    ast_position = observer.at(t).observe(asteroid)
    x, y, z = ast_position.apparent().position.au
    return [row['time'], x, y, z]

df = pd.read_csv('D:\\Earthquake\\DataSet\\DATASET.csv')
df['time'] = pd.to_datetime(df['time'])
df['y'] = df['time'].dt.year
df['m'] = df['time'].dt.month
df['d'] = df['time'].dt.day
df['h'] = df['time'].dt.hour
df['mm'] = df['time'].dt.minute
df['s'] = df['time'].dt.second

print(df.head())

eph = load('de421.bsp')
earth = eph['earth']
observer = earth + Topos(latitude_degrees=0, longitude_degrees=0)
asteroid = eph['SUN']
ts = load.timescale()

def process_chunk(chunk):
    sun_pos_chunk = chunk.apply(calculate_sun_position, axis=1)
    return sun_pos_chunk.values.tolist()

num_parts = 8
chunks = np.array_split(df, num_parts)

with concurrent.futures.ThreadPoolExecutor() as executor:
    results = list(executor.map(process_chunk, chunks))

sun_pos = [item for sublist in results for item in sublist]
dt = pd.DataFrame(sun_pos, columns=['time', 'x', 'y', 'z'])
dt.to_csv('sun.csv', index=False)


print(dt)