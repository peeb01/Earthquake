import pandas as pd
import re
from concurrent.futures import ThreadPoolExecutor

import numpy as np
import pandas as pd
from astropy.coordinates import SkyCoord
from astropy.time import Time
from astroquery.jplhorizons import Horizons


df = pd.read_csv('D:\Project\Earthquake\Comets\\raw_asteroid\AsteroidCT.csv')
df['Time'] = pd.to_datetime(df['Time'])


object_planet = ['SUN', '199', '299', '399', '301', '-74', '599', '699', '433', 'Eros', 'Orus', '-49',
                       '-490', '-255', '2000016', '90000188', '90000190', '90000191', 
                        'Leucus', 'Eurybates','Polymele', 'Vesta', 'Mathilde', 'Lutetia', 'Donaldjohanson','Braille', 'Annefrank', 
                        'Bennu', 'Itokawa', '-64', 'Apophis', 'Ryugu', '-122911', 'Patroclus', 
                        '90000855', 'Dinkinesh', '20065803' , 'Gaspra', 'Ceres']

def calculate_position(obj, time):
    """
    Args: 
        obj: obj name str
        time: time (utc) format yyyy-mm-dd
    """
    try:
        epoch = Time(time)
        q = Horizons(obj, location='@0', epochs=epoch.tdb.jd)
        tab = q.vectors(refplane='earth')
        c = SkyCoord(tab['x'].quantity, tab['y'].quantity, tab['z'].quantity,
                     representation_type='cartesian', frame='icrs',
                     obstime=epoch)
        result = str(c)
        matches = re.findall(r'-?\d+\.\d+', result)
        result_list = [float(match) for match in matches]
        return result_list
    except Exception as e:
        print(f"Error calculating position for object {obj} at time {time}")
        return [99,99,99]

no_use = ['-74', '-49','-49', '-490', '-255' , '2000016', '20065803', '-64']

def process_chunk(chunk):
    chunk[['X_new', 'Y_new', 'Z_new']] = chunk.apply(
        lambda row: pd.Series(calculate_position(row['Object_Name'], row['Time'])), axis=1)
    return chunk


df = df[(df['X'] == 99) & (df['Y'] == 99) & (df['Z'] == 99) & (~df['Object_Name'].isin(no_use))]

num_threads = 8
chunks = np.array_split(df, num_threads)

with ThreadPoolExecutor(max_workers=num_threads) as executor:
    results = list(executor.map(process_chunk, chunks))


df = pd.concat(results)

df.to_csv('CLEAR1.csv', index=False)


